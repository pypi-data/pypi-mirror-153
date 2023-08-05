# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import IO, TYPE_CHECKING, Any, Callable, Dict, Optional, Tuple, Type, Union

import pytorch_lightning as pl
import torch
import transformers
from hydra.utils import get_class
from pytorch_lightning.utilities import rank_zero_info, rank_zero_warn
from transformers import PreTrainedTokenizerBase
from transformers import pipeline as hf_transformers_pipeline

from lightning_transformers.core.config import BackboneConfig, OptimizerConfig, SchedulerConfig
from lightning_transformers.core.instantiator import Instantiator

if TYPE_CHECKING:
    from transformers import AutoModel, Pipeline


class TaskTransformer(pl.LightningModule):
    """Base class for task specific transformers, wrapping pre-trained language models for downstream tasks. The
    API is built on top of AutoModel and AutoConfig, provided by HuggingFace.

    see: https://huggingface.co/transformers/model_doc/auto.html

    Args:
        downstream_model_type: The AutoModel downstream model type.
            See https://huggingface.co/transformers/model_doc/auto.html
        backbone: Config containing backbone specific arguments.
        pretrained_model_name_or_path: Huggingface model to use if backbone config not passed.
        optimizer: Config containing optimizer specific arguments.
        scheduler: Config containing scheduler specific arguments.
        instantiator: Used to instantiate objects (when using Hydra).
            If Hydra is not being used the instantiator is not required,
            and functions that use instantiation such as ``configure_optimizers`` has been overridden.
        tokenizer: The pre-trained tokenizer.
        pipeline_kwargs: Arguments required for the HuggingFace inference pipeline class.
        **model_data_kwargs: Arguments passed from the data module to the class.
    """

    def __init__(
        self,
        downstream_model_type: str,
        optimizer: OptimizerConfig = OptimizerConfig(),
        scheduler: SchedulerConfig = SchedulerConfig(),
        pretrained_model_name_or_path: Optional[str] = None,
        backbone: Optional[BackboneConfig] = None,
        instantiator: Optional[Instantiator] = None,
        tokenizer: Optional[PreTrainedTokenizerBase] = None,
        pipeline_kwargs: Optional[dict] = None,
        **model_data_kwargs,
    ) -> None:
        super().__init__()
        self.save_hyperparameters()
        model_cls: Type["AutoModel"] = get_class(downstream_model_type)
        model_path = backbone.pretrained_model_name_or_path if backbone else pretrained_model_name_or_path
        self.model = model_cls.from_pretrained(model_path, **model_data_kwargs)
        self._tokenizer = tokenizer  # necessary for hf_pipeline
        self._hf_pipeline = None
        self._hf_pipeline_kwargs = pipeline_kwargs or {}
        self.instantiator = instantiator
        self.optimizer_cfg = optimizer
        self.scheduler_cfg = scheduler

    def configure_optimizers(self) -> Dict:
        if self.instantiator is None:
            rank_zero_warn(
                "You haven't specified an optimizer or lr scheduler. "
                "Defaulting to AdamW with an lr of 1e-5 and linear warmup for 10% of steps. "
                "To change this, override ``configure_optimizers`` in the TransformerModule."
            )
            optimizer = torch.optim.AdamW(self.parameters(), lr=1e-5)
            num_training_steps, num_warmup_steps = self.compute_warmup(
                num_training_steps=-1,
                num_warmup_steps=0.1,
            )
            scheduler = transformers.get_linear_schedule_with_warmup(
                optimizer, num_warmup_steps=num_warmup_steps, num_training_steps=num_training_steps
            )
            return {
                "optimizer": optimizer,
                "lr_scheduler": {"scheduler": scheduler, "interval": "step", "frequency": 1},
            }

        optimizer = self.instantiator.optimizer(self.model, self.optimizer_cfg)
        # compute_warmup needs the datamodule to be available when `self.num_training_steps`
        # is called that is why this is done here and not in the __init__
        self.scheduler_cfg.num_training_steps, self.scheduler_cfg.num_warmup_steps = self.compute_warmup(
            num_training_steps=self.scheduler_cfg.num_training_steps,
            num_warmup_steps=self.scheduler_cfg.num_warmup_steps,
        )
        rank_zero_info(f"Inferring number of training steps, set to {self.scheduler_cfg.num_training_steps}")
        rank_zero_info(f"Inferring number of warmup steps from ratio, set to {self.scheduler_cfg.num_warmup_steps}")
        scheduler = self.instantiator.scheduler(self.scheduler_cfg, optimizer)
        return {
            "optimizer": optimizer,
            "lr_scheduler": {"scheduler": scheduler, "interval": "step", "frequency": 1},
        }

    def on_save_checkpoint(self, checkpoint: Dict[str, Any]):
        # Save tokenizer from datamodule for predictions
        if self.instantiator:
            checkpoint["instantiator"] = self.instantiator

    def on_load_checkpoint(self, checkpoint: Dict[str, Any]) -> None:
        if "tokenizer" in checkpoint:
            self.tokenizer = checkpoint["tokenizer"]
        self.instantiator = checkpoint.get("instantiator")

    @property
    def num_training_steps(self) -> int:
        return self.trainer.estimated_stepping_batches

    def compute_warmup(self, num_training_steps: int, num_warmup_steps: Union[int, float]) -> Tuple[int, int]:
        if num_training_steps < 0:
            # less than 0 specifies to infer number of training steps
            num_training_steps = self.num_training_steps
        if isinstance(num_warmup_steps, float):
            # Convert float values to percentage of training steps to use as warmup
            num_warmup_steps *= num_training_steps
        return num_training_steps, num_warmup_steps

    def setup(self, stage: Optional[str] = None) -> None:
        self.configure_metrics(stage)

    def configure_metrics(self, stage: str) -> Optional[Any]:
        """Override to configure metrics for train/validation/test.

        This is called on fit start to have access to the data module, and initialize any data specific metrics.
        """
        pass

    @property
    def tokenizer(self) -> Optional["PreTrainedTokenizerBase"]:
        if (
            self._tokenizer is None
            and hasattr(self, "trainer")  # noqa: W503
            and hasattr(self.trainer, "datamodule")  # noqa: W503
            and hasattr(self.trainer.datamodule, "tokenizer")  # noqa: W503
        ):
            self._tokenizer = self.trainer.datamodule.tokenizer
        return self._tokenizer

    @tokenizer.setter
    def tokenizer(self, tokenizer: "PreTrainedTokenizerBase") -> None:
        self._tokenizer = tokenizer

    @property
    def hf_pipeline_task(self) -> Optional[str]:
        """Override to define what HuggingFace pipeline task to use.

        Returns: Optional string to define what pipeline task to use.
        """
        return None

    @property
    def hf_pipeline(self) -> "Pipeline":
        if self._hf_pipeline is None:
            if self.hf_pipeline_task is not None:
                self._hf_pipeline = hf_transformers_pipeline(
                    task=self.hf_pipeline_task, model=self.model, tokenizer=self.tokenizer, **self._hf_pipeline_kwargs
                )
            else:
                raise RuntimeError("No task was defined for this model. Try overriding `hf_pipeline_task`")
        return self._hf_pipeline

    @hf_pipeline.setter
    def hf_pipeline(self, pipeline: "Pipeline") -> None:
        self._hf_pipeline = pipeline

    def hf_predict(self, *args, **kwargs) -> Any:
        return self.hf_pipeline(*args, **kwargs)

    @classmethod
    def load_from_checkpoint(
        cls,
        checkpoint_path: Union[str, IO],
        map_location: Optional[Union[Dict[str, str], str, torch.device, int, Callable]] = None,
        hparams_file: Optional[str] = None,
        strict: bool = True,
        hf_pipeline_kwargs: Optional[Dict] = None,
        **kwargs,
    ):
        model: TaskTransformer = super().load_from_checkpoint(checkpoint_path, map_location, hparams_file, strict)
        # update model with hf_pipeline_kwargs override
        if hf_pipeline_kwargs is not None:
            model._hf_pipeline_kwargs.update(hf_pipeline_kwargs)
        return model
