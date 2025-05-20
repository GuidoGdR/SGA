from main import App
from tkinter.messagebox import askyesno

def cancel_for_changes_protection(app:App)->bool:
    
    if app.get_state("have_changes"):
        discard_changes = askyesno("Cambios NO guardados", "¿desea descartar los cambios ralizados?")

        if discard_changes:
            return False
        
        return True
    
    return False
