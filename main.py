import streamlit as st
import asyncio
import ollama

# Template pour la génération de matériaux
material_generation_template = """
Create a Blender Python script for a material based on the following criteria:  
**Material Type:** {material_type}  
**Base Color:** {base_color}  
**Roughness:** {roughness}  
**Metallic:** {metallic}  
**Transparency:** {transparency}  
**Emission Color:** {emission_color}  
**Special Effects:** {special_effects}  
**Prompt:** {user_prompt}  

For the following criteria, you can only reply with one option:  
- Material Type  
- Roughness  
- Metallic  
- Transparency  

For colors criteria (Base Color and Emission Color), you can choose up to three RGB colors in the format: (x,y,z).  

You can choose multiple options for:  
- Special Effects

If any of the criteria are set to None, ignore them completely and do not include them in the generated code.

**No Extra Content:** Do not include any additional text, comments, or explanations in your response.  
**Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text.  
"""

# Template pour la génération de textures
texture_generation_template = """
Create a Blender Python script for a texture based on the following criteria:  
**Texture Type:** {texture_type}  
**Mapping:** {mapping}  
**Scale:** {scale}  
**Normal Map:** {normal_map}  
**Bump Map:** {bump_map}  
**Special Effects:** {special_effects}  
**Prompt:** {user_prompt}  

Only one option accepted for:  
- Texture Type  
- Mapping  
- Scale  

For colors criteria (Normal Map and Bump Map), you can choose up to three RGB colors in the format: (x,y,z).  

You can choose multiple options for:  
- Special Effects

If any of the criteria are set to None, ignore them completely and do not include them in the generated code.

**No Extra Content:** Do not include any additional text, comments, or explanations in your response.  
**Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text.  
"""

# Template pour obtenir des recommandations pour les réglages du matériau ou de la texture
recommendation_template = """
Based on the following prompt, give recommendations for the material or texture settings (material type, base color, etc.) to achieve the best results:  

**Prompt:** {user_prompt}  

**Material Type Options:** ["Principled BSDF", "Diffuse", "Emission", "Transparent"]  
**Base Color Options:** "rgb(0, 0, 0)", "rgb(255, 255, 255)", and more  
**Roughness Options:** ["Low", "Medium", "High"]  
**Metallic Options:** [0, 0.5, 1]  
**Transparency Options:** ["Opaque", "Transparent", "Semi-Transparent"]  
**Emission Color Options:** Any valid RGB hex color code  
**Special Effects Options:** ["Glow", "Reflection", "Refraction", "Translucent"]

**Texture Type Options:** ["Noise", "Voronoi", "Image", "Checker"]  
**Mapping Options:** ["UV", "Object", "Generated", "Camera"]  
**Scale Options:** ["Low", "Medium", "High"]  
**Normal Map Options:** Any valid RGB hex color code  
**Bump Map Options:** Any valid RGB hex color code  
**Special Effects Options:** ["Distortion", "Noise", "Tiling"]  

For the following criteria, you can only reply with one option:  
- Material Type  
- Roughness  
- Metallic  
- Transparency  
- Texture Type  
- Mapping  
- Scale  

For colors criteria (Base Color, Emission Color, Normal Map, and Bump Map), you can choose up to three RGB colors in the format: (x,y,z).  

You can choose multiple options for:  
- Special Effects

**No Extra Content:** Do not include any additional text, comments, or explanations in your response.  
**Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text.  
"""

# Template pour modifier le code du matériau ou de la texture
modification_template = """
Modify the following Blender Python script for material or texture generation based on these criteria:  

**Existing Code:** {existing_code}  
**Modification Request:** {modification_prompt}  

**No Extra Content:** Do not include any additional text, comments, or explanations in your response.  
**Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text.  
"""

# Fonction pour générer le code de matériau
async def generate_material_code(prompt, material_type, base_color, roughness, metallic, transparency, emission_color, special_effects):
    full_prompt = material_generation_template.format(
        material_type=material_type or 'None',
        base_color=base_color or 'None',
        roughness=roughness or 'None',
        metallic=metallic or 'None',
        transparency=transparency or 'None',
        emission_color=emission_color or 'None',
        special_effects=special_effects or 'None',
        user_prompt=prompt
    )

    try:
        response = ollama.chat(model="llama-3.1", messages=[{"role": "user", "content": full_prompt}])
        return response['text']
    except Exception as e:
        st.error(f"Error with Ollama while generating material code: {str(e)}")
        return None

# Fonction pour générer le code de texture
async def generate_texture_code(prompt, texture_type, mapping, scale, normal_map, bump_map, special_effects):
    full_prompt = texture_generation_template.format(
        texture_type=texture_type or 'None',
        mapping=mapping or 'None',
        scale=scale or 'None',
        normal_map=normal_map or 'None',
        bump_map=bump_map or 'None',
        special_effects=special_effects or 'None',
        user_prompt=prompt
    )

    try:
        response = ollama.chat(model="llama-3.1", messages=[{"role": "user", "content": full_prompt}])
        return response['text']
    except Exception as e:
        st.error(f"Error with Ollama while generating texture code: {str(e)}")
        return None

# Fonction pour obtenir des recommandations d'Ollama
async def get_recommendations(user_prompt):
    full_prompt = recommendation_template.format(user_prompt=user_prompt)

    try:
        response = ollama.chat(model="llama-3.1", messages=[{"role": "user", "content": full_prompt}])
        return response['text']
    except Exception as e:
        st.error(f"Error with Ollama while getting recommendations: {str(e)}")
        return None

# Fonction pour modifier le code du matériau ou de la texture
async def modify_material_or_texture_code(existing_code, modification_prompt):
    full_prompt = modification_template.format(
        existing_code=existing_code,
        modification_prompt=modification_prompt
    )

    try:
        response = ollama.chat(model="llama-3.1", messages=[{"role": "user", "content": full_prompt}])
        return response['text']
    except Exception as e:
        st.error(f"Error with Ollama while modifying code: {str(e)}")
        return None

# Frontend de l'application Streamlit
st.title("AI Material and Texture Generator for Blender")

# Ajout du lien d'accès et des instructions d'utilisation dans la barre latérale
st.sidebar.subheader("Access the App")
st.sidebar.write("Click [here](http://localhost:8501) to access the app.")

st.sidebar.subheader("How to Use the App")
st.sidebar.write("""
This app allows you to create and modify Blender Python scripts for materials and textures.  
1. Select whether you want to create a material or a texture.
2. Customize the material or texture settings by selecting from dropdowns and color pickers.
3. Enter a detailed prompt to guide the AI in generating the Blender code.
4. Get AI-generated recommendations to refine your choices.
5. Generate the Blender code based on your choices, and modify it as needed.
6. Save the generated code and use it in Blender!
""")

# Sélection pour la création de matériau ou de texture
material_or_texture = st.radio("Select the type of creation", ["Material", "Texture"])

if material_or_texture == "Material":
    # Sélection du type de matériau
    material_type = st.selectbox("Select Material Type", ["Principled BSDF", "Diffuse", "Emission", "Transparent"], index=0)

    # Sélection de la couleur de base (trois sélecteurs de couleur)
    base_color_r = st.slider("Base Color Red", 0, 255, 0)
    base_color_g = st.slider("Base Color Green", 0, 255, 0)
    base_color_b = st.slider("Base Color Blue", 0, 255, 0)
    base_color = f"rgb({base_color_r}, {base_color_g}, {base_color_b})" if (base_color_r or base_color_g or base_color_b) != 0 else None

    # Réglage de la rugosité
    roughness = st.selectbox("Roughness", ["Low", "Medium", "High"], index=0)

    # Réglage métallique
    metallic = st.selectbox("Metallic", [0, 0.5, 1], index=0)

    # réglage de la transparence
    transparency = st.selectbox("Transparency", ["Opaque", "Transparent", "Semi-Transparent"], index=0)

    # Couleur d'émission (si sélectionnée)
    emission_color = st.color_picker("Emission Color", "#ff0000") if base_color != None else None

    # Effets spéciaux pour le matériau
    special_effects = st.multiselect("Special Effects", ["Glow", "Reflection", "Refraction", "Translucent"])

elif material_or_texture == "Texture":
    # Sélection du type de texture
    texture_type = st.selectbox("Select Texture Type", ["Noise", "Voronoi", "Image", "Checker"], index=0)

    # Sélection du type de mapping
    mapping = st.selectbox("Select Mapping", ["UV", "Object", "Generated", "Camera"], index=0)

    # Échelle de texture
    scale = st.selectbox("Texture Scale", ["Low", "Medium", "High"], index=0)

    # Carte normale
    normal_map = st.color_picker("Normal Map Color", "#808080") if scale != None else None

    # Carte de relief
    bump_map = st.color_picker("Bump Map Color", "#d3d3d3") if scale != None else None

    # Effets spéciaux pour la texture
    special_effects = st.multiselect("Special Effects", ["Distortion", "Noise", "Tiling"])

# Demande utilisateur pour la création de matériau ou de texture
user_prompt = st.text_area("Enter the material or texture description (e.g., 'A shiny metallic surface' or 'A rocky texture with cracks')")

# Bouton pour obtenir des recommandations pour les paramètres basés sur l'invite
if st.button("Get Settings Recommendations"):
    if user_prompt:
        try:
            recommendations = asyncio.run(get_recommendations(user_prompt))
            if recommendations:
                st.subheader("Settings Recommendations")
                st.write(recommendations)

                # Bouton pour accepter les recommandations
                if st.button("Accept Recommendations"):
                    # Analyser les recommandations et définir les valeurs dynamiquement
                    recommendation_lines = recommendations.split("\n")
                    for line in recommendation_lines:
                        if "Material Type:" in line:
                            material_type = line.split(":", 1)[1].strip()
                        elif "Base Color:" in line:
                            base_color = line.split(":", 1)[1].strip()
                        elif "Roughness:" in line:
                            roughness = line.split(":", 1)[1].strip()
                        elif "Metallic:" in line:
                            metallic = float(line.split(":", 1)[1].strip())
                        elif "Transparency:" in line:
                            transparency = line.split(":", 1)[1].strip()
                        elif "Emission Color:" in line:
                            emission_color = line.split(":", 1)[1].strip()
                        elif "Special Effects:" in line:
                            special_effects = [effect.strip() for effect in line.split(":", 1)[1].split(",")]
                        elif "Texture Type:" in line:
                            texture_type = line.split(":", 1)[1].strip()
                        elif "Mapping:" in line:
                            mapping = line.split(":", 1)[1].strip()
                        elif "Scale:" in line:
                            scale = line.split(":", 1)[1].strip()
                        elif "Normal Map:" in line:
                            normal_map = line.split(":", 1)[1].strip()
                        elif "Bump Map:" in line:
                            bump_map = line.split(":", 1)[1].strip()
                        elif "Special Effects:" in line:
                            special_effects = [effect.strip() for effect in line.split(":", 1)[1].split(",")]
        except Exception as e:
            st.error(f"Error while processing recommendations: {str(e)}")

# Bouton pour générer le code de matériau ou de texture basé sur l'invite et les paramètres
if st.button("Generate Material or Texture Code"):
    if user_prompt:
        try:
            if material_or_texture == "Material":
                material_code = asyncio.run(generate_material_code(
                    user_prompt,
                    material_type,
                    base_color,
                    roughness,
                    metallic,
                    transparency,
                    emission_color,
                    special_effects
                ))

                if material_code:
                    st.subheader("Generated Material Code:")
                    st.code(material_code)

                    # Activer la fonctionnalité de modification si le code de matériau est généré
                    modification_prompt = st.text_area("Enter modification request for the material code")
                    if st.button("Modify Material Code"):
                        if modification_prompt:
                            modified_code = asyncio.run(modify_material_or_texture_code(material_code, modification_prompt))
                            if modified_code:
                                material_code = modified_code  # Mettre à jour la variable de code du matériau avec le code modifié
                                st.subheader("Modified Material Code:")
                                st.code(modified_code)

            elif material_or_texture == "Texture":
                texture_code = asyncio.run(generate_texture_code(
                    user_prompt,
                    texture_type,
                    mapping,
                    scale,
                    normal_map,
                    bump_map,
                    special_effects
                ))

                if texture_code:
                    st.subheader("Generated Texture Code:")
                    st.code(texture_code)

                    # Activer la fonctionnalité de modification si le code de texture est généré
                    modification_prompt = st.text_area("Enter modification request for the texture code")
                    if st.button("Modify Texture Code"):
                        if modification_prompt:
                            modified_code = asyncio.run(modify_material_or_texture_code(texture_code, modification_prompt))
                            if modified_code:
                                texture_code = modified_code  # Mettre à jour la variable du code de texture avec le code modifié
                                st.subheader("Modified Texture Code:")
                                st.code(modified_code)

        except Exception as e:
            st.error(f"Error while generating or modifying code: {str(e)}")

# Pied de page ou instructions supplémentaires de l'application
st.sidebar.subheader("About this app")
st.sidebar.write("""
This AI-powered app helps you create and modify Blender Python scripts for materials and textures.  
You can select from various material and texture types and customize properties like color, roughness, scale, and more.  
Once you generate the code, you can modify it to meet your specific needs.  
For any issues, you can generate new recommendations or modify existing code as required.
Florian Gionnane, Darkstar Games 
""")

