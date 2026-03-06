from .rlc_json_to_prompt import RLCJsonToPrompt
from .rlc_seed_vault_pro import RLCSeedVaultPro

NODE_CLASS_MAPPINGS = {
    "RLCJsonToPrompt": RLCJsonToPrompt,
    "RLCSeedVaultPro": RLCSeedVaultPro
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RLCJsonToPrompt": "RLC Json to Prompt 🔄",
    "RLCSeedVaultPro": "RLC Seed Vault Pro 📚"
}

__version__ = "1.0.0"