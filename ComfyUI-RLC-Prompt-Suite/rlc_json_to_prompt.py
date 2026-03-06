import json
import re

class UniversalJsonToPrompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_text": ("STRING", {"multiline": True, "default": "{}"}),
                "prompt_format": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                # Ana kategoriler - her biri için alternatif anahtar yolları
                "subject_keys": ("STRING", {"default": "subject, person, character, model, identity"}),
                "hair_keys": ("STRING", {"default": "subject.hair, subject.hair.color, subject.hair.style, subject.facial_features.hair, wardrobe.hair, hair"}),
                "skin_keys": ("STRING", {"default": "subject.skin, subject.body.skin_tone, subject.facial_features.skin, skin_tone, skin"}),
                "body_keys": ("STRING", {"default": "subject.body, subject.body.physique, subject.body.details, body, physique"}),
                "face_keys": ("STRING", {"default": "subject.facial_features, face, facial_features, subject.face"}),
                
                # Kıyafet ve aksesuar
                "clothing_top_keys": ("STRING", {"default": "wardrobe.top, clothing.top, outfit.top, top"}),
                "clothing_bottom_keys": ("STRING", {"default": "wardrobe.bottom, clothing.bottom, outfit.bottom, bottom"}),
                "accessories_keys": ("STRING", {"default": "wardrobe.accessories, accessories, jewelry, outfit.accessories"}),
                
                # Poz
                "pose_keys": ("STRING", {"default": "pose_action, pose, pose_action.description, pose.details, action"}),
                
                # Mekan ve arka plan
                "location_keys": ("STRING", {"default": "scene.location, scene, location, environment, setting"}),
                "background_keys": ("STRING", {"default": "scene.background_elements, background, scene_elements, backdrop"}),
                
                # Işık
                "lighting_keys": ("STRING", {"default": "lighting, lighting.setup, lighting.details, light"}),
                
                # Kamera
                "camera_keys": ("STRING", {"default": "camera, camera.perspective, camera.technical, photography"}),
                
                # Vibe ve atmosfer
                "mood_keys": ("STRING", {"default": "mood, atmosphere, vibe, scene.environment"}),
                
                # Özel flag'ler
                "reflection_rules": ("STRING", {"default": "camera.reflection_integrity_rules, reflection_rules, mirror_rules"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "convert"
    CATEGORY = "custom/prompt"

    def get_value(self, data, key_paths, default=""):
        """Birden çok anahtar yolunu dene, ilk bulunanı döndür"""
        paths = [p.strip() for p in key_paths.split(',')]
        
        for path in paths:
            try:
                # Noktalı yolu parçala (örn: "subject.hair.color")
                parts = path.split('.')
                value = data
                for part in parts:
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        raise KeyError
                
                # Eğer değer string'sa döndür
                if isinstance(value, str):
                    return value
                # Eğer değer dict'sa, string'e çevir
                elif isinstance(value, dict):
                    return str(value)
                # Eğer değer listeyse, birleştir
                elif isinstance(value, list):
                    return ', '.join([str(v) for v in value])
                    
            except (KeyError, TypeError):
                continue
        
        return default

    def extract_all_placeholders(self, format_str):
        """Format string'indeki tüm {placeholder}ları bul"""
        return re.findall(r'\{([^}]+)\}', format_str)

    def convert(self, json_text, prompt_format, **kwargs):
        try:
            # JSON'u parse et
            data = json.loads(json_text)
            
            # Eğer prompt_format boşsa, default bir format oluştur
            if not prompt_format.strip():
                prompt_format = self.create_default_format(data)
            
            # Tüm placeholder'ları bul
            placeholders = self.extract_all_placeholders(prompt_format)
            
            # Her placeholder için değer bul
            result = prompt_format
            for placeholder in placeholders:
                # Placeholder ismine göre uygun key listesini seç
                key_list_name = self.get_key_list_name(placeholder)
                
                if key_list_name and key_list_name in kwargs:
                    value = self.get_value(data, kwargs[key_list_name])
                else:
                    # Bilinmeyen placeholder için direkt JSON'da ara
                    value = self.get_value(data, placeholder)
                
                # Yerine koy
                result = result.replace(f"{{{placeholder}}}", value)
            
            return (result,)
            
        except Exception as e:
            return (f"Error: {str(e)}",)
    
    def get_key_list_name(self, placeholder):
        """Placeholder ismine göre hangi key listesinin kullanılacağını belirle"""
        mapping = {
            # Subject
            'subject': 'subject_keys',
            'person': 'subject_keys',
            'character': 'subject_keys',
            
            # Hair
            'hair': 'hair_keys',
            'hair_color': 'hair_keys',
            'hair_style': 'hair_keys',
            
            # Skin
            'skin': 'skin_keys',
            'skin_tone': 'skin_keys',
            'complexion': 'skin_keys',
            
            # Body
            'body': 'body_keys',
            'physique': 'body_keys',
            'figure': 'body_keys',
            
            # Face
            'face': 'face_keys',
            'facial_features': 'face_keys',
            
            # Clothing
            'top': 'clothing_top_keys',
            'clothing_top': 'clothing_top_keys',
            'bottom': 'clothing_bottom_keys',
            'clothing_bottom': 'clothing_bottom_keys',
            'accessories': 'accessories_keys',
            'jewelry': 'accessories_keys',
            
            # Pose
            'pose': 'pose_keys',
            'action': 'pose_keys',
            'pose_action': 'pose_keys',
            
            # Location
            'location': 'location_keys',
            'scene': 'location_keys',
            'environment': 'location_keys',
            
            # Background
            'background': 'background_keys',
            'backdrop': 'background_keys',
            'scene_elements': 'background_keys',
            
            # Lighting
            'lighting': 'lighting_keys',
            'light': 'lighting_keys',
            'illumination': 'lighting_keys',
            
            # Camera
            'camera': 'camera_keys',
            'photography': 'camera_keys',
            'shot': 'camera_keys',
            
            # Mood
            'mood': 'mood_keys',
            'atmosphere': 'mood_keys',
            'vibe': 'mood_keys',
            
            # Special
            'reflection': 'reflection_rules',
            'mirror': 'reflection_rules',
        }
        
        return mapping.get(placeholder.lower(), None)
    
    def create_default_format(self, data):
        """JSON yapısına göre otomatik bir format oluştur"""
        format_parts = []
        
        # Subject description
        desc = self.get_value(data, "subject.description, person.description, description")
        if desc:
            format_parts.append(desc)
        
        # Hair
        hair = self.get_value(data, "subject.hair, subject.hair.color, subject.hair.style, hair")
        if hair:
            format_parts.append(f"{hair} hair")
        
        # Body
        body = self.get_value(data, "subject.body.physique, subject.body.details, body, physique")
        if body:
            format_parts.append(str(body))
        
        # Clothing
        top = self.get_value(data, "wardrobe.top, clothing.top, top")
        if top:
            format_parts.append(f"wearing {top}")
        
        bottom = self.get_value(data, "wardrobe.bottom, clothing.bottom, bottom")
        if bottom:
            format_parts.append(bottom)
        
        # Pose
        pose = self.get_value(data, "pose_action.description, pose, pose.details, action")
        if pose:
            format_parts.append(str(pose))
        
        # Location
        location = self.get_value(data, "scene.location, scene, location, environment")
        if location:
            format_parts.append(f"in {location}")
        
        # Lighting
        lighting = self.get_value(data, "lighting.setup, lighting, lighting.details, light")
        if lighting:
            format_parts.append(f"with {lighting}")
        
        # Camera
        camera = self.get_value(data, "camera.technical, camera, photography")
        if camera:
            format_parts.append(str(camera))
        
        return ". ".join(format_parts) + "."

# Node'u kaydet
NODE_CLASS_MAPPINGS = {
    "RLCJsonToPrompt": UniversalJsonToPrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RLCJsonToPrompt": "RLC JSON to Prompt"
}
CATEGORY = "RLC Prompt Suite"