import c4d
import os
from c4d import gui

# Python Tag code
TAG_CODE = """import c4d

def main():
    # Safely get the document from the tag itself
    doc = op.GetDocument()
    if not doc:
        return

    # Get the specific viewport designated as the Render View
    render_bd = doc.GetRenderBaseDraw()
    if not render_bd:
        return
        
    # Get the camera currently driving the Render View
    render_active_cam = render_bd.GetSceneCamera(doc)
    
    # Update Camera Visibility
    cam_type = c4d.Ocamera
    vis_id = c4d.ID_BASEOBJECT_VISIBILITY_EDITOR
    vis_undef = c4d.OBJECT_UNDEF
    vis_off = c4d.OBJECT_OFF
    
    # Iterative (non-recursive) hierarchy traversal
    current_obj = doc.GetFirstObject()
    while current_obj:
        if current_obj.GetType() == cam_type:
            
            # Visible if it's the render view camera, hidden otherwise
            target_vis = vis_undef if current_obj == render_active_cam else vis_off
            
            if current_obj[vis_id] != target_vis:
                current_obj[vis_id] = target_vis
        
        # Move to next object without recursion
        if current_obj.GetDown():
            current_obj = current_obj.GetDown()
        else:
            while not current_obj.GetNext() and current_obj.GetUp():
                current_obj = current_obj.GetUp()
            current_obj = current_obj.GetNext()
"""

def get_script_info():
    """Finds the script's name and associated icon file."""
    try:
        script_path = __file__
        base_path = os.path.splitext(script_path)[0]
        script_name = os.path.basename(base_path)
        
        for ext in [".tif", ".png", ".jpg"]:
            icon_path = base_path + ext
            if os.path.exists(icon_path):
                return script_name, icon_path
                
        return script_name, None
    except NameError:
        return "Hide Cams by Render View", None

def main():
    active_obj = doc.GetActiveObject()
    
    if not active_obj:
        gui.MessageDialog("Please select an object to attach the tag to.")
        return
    
    doc.StartUndo()
    
    # Create a new Python Tag
    python_tag = c4d.BaseTag(c4d.Tpython)
    python_tag[c4d.TPYTHON_CODE] = TAG_CODE
    
    # Fetch script name and icon path
    script_name, icon_path = get_script_info()
    
    # Set the tag name dynamically
    python_tag.SetName(script_name)
    
    # Apply the icon and force normalization
    if icon_path:
        python_tag[c4d.ID_BASELIST_ICON_FILE] = str(os.path.normpath(icon_path))
    
    active_obj.InsertTag(python_tag)
    
    # Force the tag to refresh its internal state
    python_tag.Message(c4d.MSG_UPDATE)
    python_tag.Message(c4d.MSG_CHANGE)
    
    doc.AddUndo(c4d.UNDOTYPE_NEW, python_tag)
    doc.EndUndo()
    
    c4d.EventAdd()

if __name__=='__main__':
    main()