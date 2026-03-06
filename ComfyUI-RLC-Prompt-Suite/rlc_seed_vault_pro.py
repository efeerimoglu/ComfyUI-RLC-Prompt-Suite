import json
import os
import time
from PIL import Image
import numpy as np
import folder_paths

class SeedVaultPro:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "images": ("IMAGE",),
                "mode": (["auto_save", "manual_save", "update_only"], {"default": "auto_save"}),
                "prompt_summary": ("STRING", {"default": "", "multiline": False}),
                "notes": ("STRING", {"default": "", "multiline": True}),
                "rating": ("INT", {"default": 5, "min": 1, "max": 10, "step": 1}),
                "tags": ("STRING", {"default": "", "multiline": False}),
                "cfg": ("FLOAT", {"default": 5.5, "min": 1.0, "max": 20.0}),
                "steps": ("INT", {"default": 30, "min": 1, "max": 100}),
                "sampler": ("STRING", {"default": "dpmpp_sde"}),
                "clip_skip": ("INT", {"default": 2, "min": 1, "max": 12, "step": 1}),
                "hyperlora": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0}),
                "instantid": ("FLOAT", {"default": 0.55, "min": 0.0, "max": 2.0}),
                "controlnet": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0}),
                "save_image": ("BOOLEAN", {"default": True}),
                "approve": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "vault_path": ("STRING", {"default": "ComfyUI/output/seed_vault/"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "IMAGE")
    RETURN_NAMES = ("vault_output", "json_output", "preview")
    FUNCTION = "save_seed"
    CATEGORY = "📚 Seed Vault"

    def save_seed(self, seed, images, mode, prompt_summary, notes, rating, tags, 
                  cfg, steps, sampler, clip_skip, hyperlora, instantid, controlnet, 
                  save_image, approve, vault_path="ComfyUI/output/seed_vault/"):
        
        # Klasörleri oluştur
        os.makedirs(vault_path, exist_ok=True)
        os.makedirs(os.path.join(vault_path, "images"), exist_ok=True)
        os.makedirs(os.path.join(vault_path, "thumbnails"), exist_ok=True)
        
        # Zaman damgası
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        date_str = time.strftime("%Y%m%d_%H%M%S")
        
        # Database dosyası
        db_path = os.path.join(vault_path, "seed_database.json")
        
        # Mevcut database'i yükle
        if os.path.exists(db_path):
            with open(db_path, 'r', encoding='utf-8') as f:
                try:
                    db = json.load(f)
                except:
                    db = {"seeds": []}
        else:
            db = {"seeds": []}
        
        # Görsel kaydetme işlemi
        image_saved = False
        image_path = "Not saved"
        thumb_path = ""
        
        if mode == "auto_save" and save_image and images is not None:
            image_saved, image_path, thumb_path = self.save_images(images, seed, date_str, vault_path)
        
        elif mode == "manual_save" and approve and save_image and images is not None:
            image_saved, image_path, thumb_path = self.save_images(images, seed, date_str, vault_path)
        
        elif mode == "update_only":
            image_saved = False
            image_path = "Not saved (update only)"
            thumb_path = ""
        
        # Yeni seed kaydı
        new_entry = {
            "id": str(seed),
            "date": timestamp,
            "mode": mode,
            "prompt_summary": prompt_summary,
            "notes": notes,
            "rating": rating,
            "tags": [t.strip() for t in tags.split(",") if t.strip()],
            "settings": {
                "cfg": cfg,
                "steps": steps,
                "sampler": sampler,
                "clip_skip": clip_skip,
                "hyperlora": hyperlora,
                "instantid": instantid,
                "controlnet": controlnet
            },
            "image": image_path if image_saved else "",
            "thumbnail": thumb_path if image_saved else ""
        }
        
        # Aynı seed varsa güncelle, yoksa ekle
        found = False
        for i, entry in enumerate(db["seeds"]):
            if entry["id"] == str(seed):
                if not image_saved and "image" in entry:
                    new_entry["image"] = entry["image"]
                    new_entry["thumbnail"] = entry.get("thumbnail", "")
                db["seeds"][i] = new_entry
                found = True
                break
        
        if not found:
            db["seeds"].append(new_entry)
        
        # Seed'leri tarihe göre sırala (yeniden eskiye)
        db["seeds"].sort(key=lambda x: x["date"], reverse=True)
        
        # Database'i kaydet
        try:
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(db, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Database save failed: {e}")
        
        # Show Text için çıktı oluştur
        output_lines = []
        output_lines.append("═" * 60)
        output_lines.append(f"          📚 SEED VAULT PRO ({len(db['seeds'])} seeds)")
        output_lines.append("═" * 60)
        output_lines.append("")
        
        for entry in db["seeds"][:20]:
            current_rating = entry.get("rating", 5)
            star = "⭐" if current_rating >= 8 else "📌" if current_rating >= 5 else "⚠️"
            mode_icon = "🤖" if entry.get("mode") == "auto_save" else "✍️" if entry.get("mode") == "manual_save" else "🔄"
            
            output_lines.append(f"{star} {mode_icon} {entry['id']} | {entry['date'][:16]} | ⭐ {current_rating}/10")
            
            if entry.get("prompt_summary"):
                output_lines.append(f"   📝 {entry['prompt_summary']}")
            
            if entry.get("notes"):
                output_lines.append(f"   💬 {entry['notes']}")
            
            output_lines.append(f"   ⚙️ CFG:{entry['settings']['cfg']} | ST:{entry['settings']['steps']} | CS:{entry['settings']['clip_skip']} | HL:{entry['settings']['hyperlora']} | ID:{entry['settings']['instantid']} | CN:{entry['settings']['controlnet']}")
            
            if entry.get("tags") and entry["tags"]:
                output_lines.append(f"   🏷️ {', '.join(entry['tags'])}")
            
            if entry.get("image") and entry["image"] != "Not saved" and entry["image"] != "Not saved (update only)" and entry["image"] != "":
                output_lines.append(f"   🖼️ {os.path.basename(entry['image'])}")
            
            output_lines.append("")
        
        output_lines.append("═" * 60)
        output_lines.append("📌 MODES:")
        output_lines.append("   🤖 auto_save  : Automatically save every run")
        output_lines.append("   ✍️ manual_save : Save only when approved (use approve button)")
        output_lines.append("   🔄 update_only : Update notes only (no image saved)")
        output_lines.append("")
        output_lines.append("💡 TIP: Bypass Face Detailer/Save Image nodes")
        output_lines.append("   to run only Seed Vault without regenerating images.")
        output_lines.append("═" * 60)
        
        vault_output = "\n".join(output_lines)
        json_output = json.dumps(db, indent=2, ensure_ascii=False)
        
        return (vault_output, json_output, images)
    
    def save_images(self, images, seed, date_str, vault_path):
        try:
            image_filename = f"seed_{seed}_{date_str}.png"
            thumb_filename = f"thumb_{seed}_{date_str}.jpg"
            image_path = os.path.join(vault_path, "images", image_filename)
            thumb_path = os.path.join(vault_path, "thumbnails", thumb_filename)
            
            img = images[0].cpu().numpy() * 255
            img = img.astype(np.uint8)
            pil_img = Image.fromarray(img)
            
            pil_img.save(image_path, "PNG")
            pil_img.thumbnail((256, 256))
            pil_img.save(thumb_path, "JPEG", quality=85)
            
            return True, image_path, thumb_path
        except Exception as e:
            print(f"Image save failed: {e}")
            return False, f"Error: {str(e)}", ""

NODE_CLASS_MAPPINGS = {
    "RLCSeedVaultPro": SeedVaultPro
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RLCSeedVaultPro": "RLC Seed Vault Pro 📚"
}
CATEGORY = "RLC Prompt Suite"