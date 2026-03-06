# 🚀 RLC Prompt Suite for ComfyUI

**A powerful suite of custom nodes for JSON-based prompt generation and seed management.**

---

## ✨ Features

### 🔄 RLC Json to Prompt
- **JSON to Prompt:** Convert any JSON structure to detailed prompts automatically.
- **Flexible Key Mapping:** Pre-configured with common key alternatives for subject, hair, clothing, lighting, camera, etc.
- **Custom Formats:** Create your own prompt templates with `{placeholder}` syntax.
- **Preview Any:** Compatible with all "show text" nodes.

### 📚 RLC Seed Vault Pro
- **Seed Management:** Save seeds with notes, ratings, and tags - never lose a good seed again!
- **3 Working Modes:** `auto_save`, `manual_save`, `update_only`.
- **Image Backup:** Automatically saves full images and thumbnails.
- **Settings Storage:** Saves CFG, Steps, Sampler, Clip Skip, LoRA strengths.
- **Rating System:** 1-10 rating with visual icons.

---

## 📦 Installation

### Method 1: ComfyUI Manager (Recommended)
1. Open **ComfyUI Manager**.
2. Search for `"RLC Prompt Suite"`.
3. Click **Install**.
4. **Restart** ComfyUI.

### Method 2: Manual Installation
```bash
cd ComfyUI/custom_nodes/
git clone [https://github.com/efeerimoglu/ComfyUI-RLC-Prompt-Suite.git](https://github.com/efeerimoglu/ComfyUI-RLC-Prompt-Suite.git)
```
*Restart ComfyUI after cloning.*

---

## 📋 Requirements

* ✅ **ComfyUI** (latest version)
* ✅ **WAS Node Suite** (required for Seed node)
* ✅ **Any show text node** (default PreviewAny works perfectly)

---

## 🚀 Quick Start

### 1. Try the Example Workflow
The package comes with a **ready-to-run example workflow**:
- Navigate to `ComfyUI/custom_nodes/ComfyUI-RLC-Prompt-Suite/examples/`
- Drag `RLC-Workflow.json` into ComfyUI.
- Click **Queue** - it works out of the box! ✨

### 2. Basic Usage - RLC Json to Prompt
**Example JSON:**
```json
{  
  "subject": { "hair": "long dark curly", "eyes": "brown", "skin": "fair" },  
  "clothing": { "top": "red cardigan" }
}
```
**Example Format:**
`A woman with {subject.hair} hair and {subject.eyes} eyes, {subject.skin} skin wearing {clothing.top}.`

**Output:**
*A woman with long dark curly hair and brown eyes, fair skin wearing red cardigan.*

---

## 🔧 Key Fields Reference

| Category | Default Keys (Search Order) |
| :--- | :--- |
| **Subject** | `subject`, `person`, `character`, `model`, `identity` |
| **Hair** | `subject.hair`, `subject.hair.color`, `subject.hair.style`, `hair` |
| **Skin** | `subject.skin`, `subject.body.skin_tone`, `skin_tone`, `skin` |
| **Body** | `subject.body`, `subject.body.physique`, `body`, `physique` |
| **Face** | `subject.facial_features`, `face`, `facial_features` |
| **Top Clothing** | `wardrobe.top`, `clothing.top`, `outfit.top`, `top` |
| **Bottom Clothing** | `wardrobe.bottom`, `clothing.bottom`, `outfit.bottom`, `bottom` |
| **Accessories** | `wardrobe.accessories`, `accessories`, `jewelry` |
| **Pose** | `pose_action`, `pose`, `pose_action.description`, `action` |
| **Location** | `scene.location`, `scene`, `location`, `environment`, `setting` |
| **Background** | `scene.background_elements`, `background`, `backdrop` |
| **Lighting** | `lighting`, `lighting.setup`, `lighting.details`, `light` |
| **Camera** | `camera`, `camera.perspective`, `camera.technical`, `photography` |
| **Mood** | `mood`, `atmosphere`, `vibe` |

---

## 🛠️ Usage Details - RLC Seed Vault Pro

| Mode | Icon | Description |
| :--- | :---: | :--- |
| **auto_save** | 🤖 | Automatically save every run |
| **manual_save** | ✍️ | Save only when approved |
| **update_only** | 🔄 | Update notes only (no image) |

| Field | Description |
| :--- | :--- |
| **Prompt Summary** | Short description (e.g., "Red cardigan portrait") |
| **Notes** | Detailed observations |
| **Rating** | 1-10 score with visual icons |
| **Tags** | Comma separated keywords (e.g., "portrait, red, cardigan") |


---

## ⚠️ Important Notes

### **Settings are MANUAL!**
The node does **NOT** auto-detect settings from KSampler. You must enter:
- ⚙️ **CFG Scale**
- ⚙️ **Steps**
- ⚙️ **Sampler name**
- ⚙️ **Clip Skip**
- ⚙️ **LoRA strengths**

> ❗ **Always enter the SAME values you use in KSampler!**

### **Vault Path Configuration**
The node automatically creates the `seed_vault` folder. Use **FULL PATH**:

| OS | Example Path |
| :--- | :--- |
| **Windows** | `C:/ComfyUI_windows_portable/ComfyUI/output/seed_vault/` |
| **Mac** | `/Users/username/ComfyUI/output/seed_vault/` |
| **Linux** | `/home/username/ComfyUI/output/seed_vault/` |

---

## 🗺️ Roadmap

- [x] **v1.0:** Initial release with Json to Prompt and Seed Vault Pro
- [ ] **v1.1:** Bug fixes and performance improvements (Soon)
- [ ] **v2.0:** Multi-workflow folder support, auto summary
- [ ] **v2.5:** Search and filter for seed database
- [ ] **v3.0:** Auto settings detection from KSampler (Under consideration)

---

## ❓ FAQ

**Q: Do I need to manually create the seed_vault folder?**
A: No! The node automatically creates it at your specified path.

**Q: Why aren't my settings auto-detected from KSampler?**
A: KSampler doesn't expose settings as outputs, so manual entry is required.

---

## 💬 Support & License

- **GitHub Issues:** [Link to Issues](https://github.com/efeerimoglu/ComfyUI-RLC-Prompt-Suite/issues)
- **License:** MIT License - Copyright (c) 2026 Efe Erimoğlu

<div align="center"> 
  <br>
  ⭐ **If you find this useful, please star on GitHub!** ⭐ 
</div>
