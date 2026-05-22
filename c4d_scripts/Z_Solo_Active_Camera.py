import c4d

def get_all_cameras(op):
    """Recursively find and return a list of all cameras in the object manager."""
    cameras = []
    while op:
        if op.GetType() == c4d.Ocamera:
            cameras.append(op)
        # Check children
        cameras.extend(get_all_cameras(op.GetDown()))
        # Move to next sibling
        op = op.GetNext()
    return cameras

def main():
    doc = c4d.documents.GetActiveDocument()
    
    # Get the BaseDraw (viewport) that is currently set as the Render View
    render_bd = doc.GetRenderBaseDraw()
    if not render_bd:
        render_bd = doc.GetActiveBaseDraw()
        
    # Get the active camera for the render view (accounts for Stage Objects as well)
    render_cam = render_bd.GetSceneCamera(doc)
    
    # Get the first object in the Object Manager
    first_obj = doc.GetFirstObject()
    if not first_obj:
        return
        
    # Collect all cameras in the scene
    all_cameras = get_all_cameras(first_obj)
    
    doc.StartUndo()
    
    for cam in all_cameras:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, cam)
        
        if cam == render_cam:
            # Force visibility ON (Green Dot) for the render camera
            cam[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = c4d.OBJECT_ON
        else:
            # Force visibility OFF (Red Dot) for all other cameras
            cam[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = c4d.OBJECT_OFF
            
    doc.EndUndo()
    
    # Update the scene
    c4d.EventAdd()

if __name__ == '__main__':
    main()
