import torch
import torch.nn as nn
from transformers import Qwen2_5_VLForConditionalGeneration, AutoConfig, PreTrainedModel
from transformers.models.qwen2_5_vl.modeling_qwen2_5_vl import Qwen2_5_VLCausalLMOutputWithPast
from typing import Any, Dict, List, Optional, Tuple, Union
import os

import transformers.models.qwen2_5_vl.modeling_qwen2_5_vl as qwen_modeling

from configuration_lottie_decoder import LottieDecoderConfig
from runtime import parse_torch_dtype


class LottieDecoder(PreTrainedModel):
    """
    Autoregressive generative model for OmniLottie

    Lottie animation generation model based on Qwen2.5-VL,
    supports generating Lottie JSON code from videos.
    """

    config_class = LottieDecoderConfig
    base_model_prefix = "lottie_decoder"
    supports_gradient_checkpointing = True

    def __init__(self, config: LottieDecoderConfig):
        """
        Initialize LottieDecoder model

        Args:
            config (LottieDecoderConfig): Model configuration object
        """
        super().__init__(config)

        self.config = config
        self.pix_len = config.pix_len
        self.text_len = config.text_len
        self.vocab_size = config.vocab_size
        self.bos_token_id = config.bos_token_id
        self.eos_token_id = config.eos_token_id
        self.pad_token_id = config.pad_token_id

        base_model_path = config.base_model_path
        if os.path.isabs(base_model_path) and not os.path.exists(base_model_path):
            print(
                f"Base model path {base_model_path} not found, "
                "falling back to Qwen/Qwen2.5-VL-3B-Instruct"
            )
            base_model_path = "Qwen/Qwen2.5-VL-3B-Instruct"
            self.config.base_model_path = base_model_path

        print(f"Initializing LottieDecoder with base model: {base_model_path}")

        # Create base model configuration
        qwen_config = AutoConfig.from_pretrained(
            base_model_path,
            vocab_size=self.vocab_size,
            bos_token_id=self.bos_token_id,
            eos_token_id=self.eos_token_id,
            pad_token_id=self.pad_token_id,
            trust_remote_code=True
        )

        # Load base Qwen2.5-VL model
        resolved_dtype = parse_torch_dtype(config.torch_dtype)

        if config.load_pretrained_backbone:
            self.transformer = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                base_model_path,
                config=qwen_config,
                torch_dtype=resolved_dtype,
                attn_implementation=config.attn_implementation,
                ignore_mismatched_sizes=True
            )
        else:
            qwen_config._attn_implementation = config.attn_implementation
            self.transformer = Qwen2_5_VLForConditionalGeneration(qwen_config)
            if resolved_dtype is not None:
                self.transformer = self.transformer.to(dtype=resolved_dtype)

        # Extend vocabulary to support Lottie tokens
        self.transformer.resize_token_embeddings(self.vocab_size)

        # Set to training mode initially (same as original decoder)
        self.train()

        print(f"LottieDecoder initialized successfully. Vocab size: {self.vocab_size}")

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, *model_args, **kwargs):
        """
        Load LottieDecoder from pretrained model path

        Supports two loading methods:
        1. Load from Hugging Face standard format (recommended)
        2. Load from old format pytorch_model.bin (backward compatible)
        """
        # Check if it's old format (contains pytorch_model.bin)
        if os.path.isdir(pretrained_model_name_or_path):
            old_format_path = os.path.join(pretrained_model_name_or_path, 'pytorch_model.bin')
            if os.path.exists(old_format_path) and not os.path.exists(os.path.join(pretrained_model_name_or_path, 'config.json')):
                print(f"Detected old format model, loading from {old_format_path}...")
                return cls._from_old_format(pretrained_model_name_or_path, **kwargs)

        kwargs.setdefault("load_pretrained_backbone", False)
        kwargs.setdefault("base_model_path", "Qwen/Qwen2.5-VL-3B-Instruct")

        return super().from_pretrained(pretrained_model_name_or_path, *model_args, **kwargs)

    @classmethod
    def _from_old_format(cls, checkpoint_path, **kwargs):
        """
        Load model from old format (pytorch_model.bin)

        Args:
            checkpoint_path: Directory path containing pytorch_model.bin
        """
        # Extract configuration parameters
        pix_len = kwargs.pop('pix_len', 4560)
        text_len = kwargs.pop('text_len', 1500)
        base_model_path = kwargs.pop('base_model_path', 'Qwen/Qwen2.5-VL-3B-Instruct')
        torch_dtype = kwargs.pop('torch_dtype', 'auto')
        attn_implementation = kwargs.pop('attn_implementation', 'eager')

        # Create configuration
        config = LottieDecoderConfig(
            pix_len=pix_len,
            text_len=text_len,
            base_model_path=base_model_path,
            torch_dtype=torch_dtype,
            attn_implementation=attn_implementation,
            load_pretrained_backbone=False,
        )

        # Initialize model
        model = cls(config)

        # Load weights
        model_file = os.path.join(checkpoint_path, 'pytorch_model.bin')
        if os.path.exists(model_file):
            state_dict = torch.load(model_file, map_location='cpu')
            model.load_state_dict(state_dict, strict=False)
            print(f"Successfully loaded weights from {model_file}")
        else:
            print(f"Warning: Model file not found {model_file}")

        return model

    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        pixel_values=None,
        image_grid_thw=None,
        pixel_values_videos=None,
        video_grid_thw=None,
        labels=None,
        past_key_values=None,
        use_cache=False,
        **kwargs
    ):
        """
        Forward pass - currently for inference only, needs implementation for training
        """
        return self.transformer(
            input_ids=input_ids,
            attention_mask=attention_mask,
            pixel_values=pixel_values,
            image_grid_thw=image_grid_thw,
            pixel_values_videos=pixel_values_videos,
            video_grid_thw=video_grid_thw,
            labels=labels,
            past_key_values=past_key_values,
            use_cache=use_cache,
            **kwargs
        )

    def generate(self, *args, **kwargs):
        """
        Generate Lottie tokens

        Directly calls the underlying transformer's generate method
        """
        return self.transformer.generate(*args, **kwargs)

    def get_input_embeddings(self):
        """Get input embeddings"""
        return self.transformer.get_input_embeddings()

    def set_input_embeddings(self, value):
        """Set input embeddings"""
        self.transformer.set_input_embeddings(value)

    def get_output_embeddings(self):
        """Get output embeddings"""
        return self.transformer.get_output_embeddings()

    def set_output_embeddings(self, new_embeddings):
        """Set output embeddings"""
        self.transformer.set_output_embeddings(new_embeddings)

    def resize_token_embeddings(self, new_num_tokens: Optional[int] = None):
        """Resize token embeddings"""
        return self.transformer.resize_token_embeddings(new_num_tokens)
