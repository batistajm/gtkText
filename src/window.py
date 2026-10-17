import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

@Gtk.Template(resource_path='/com/github/batistajm/gtkText/window.ui')
class GtkTextWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'GtkTextWindow'

    # Liaison des widgets définis dans le XML par leur ID respectif
    zone_texte = Gtk.Template.Child()
    label_info = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Texte de bienvenue par défaut dans le Buffer
        buffer = self.zone_texte.get_buffer()
        buffer.set_text("Bienvenue dans PyText !\nTapez ou ouvrez un fichier texte.")

    # --- ACTION : OUVRIR UN FICHIER ---
    @Gtk.Template.Callback()
    def on_bouton_ouvrir_clicked(self, button):
        dialog = Gtk.FileDialog.new()
        dialog.set_title("Ouvrir un fichier texte")
        # On affiche la fenêtre de dialogue liée de manière asynchrone à notre fenêtre (self)
        dialog.open(self, None, self.on_open_response)

    def on_open_response(self, dialog, result):
        try:
            gfile = dialog.open_finish(result)
            chemin_absolu = gfile.get_path()

            # Lecture du fichier avec la fonction standard de Python
            with open(chemin_absolu, 'r', encoding='utf-8') as f:
                contenu_lu = f.read()

            # Injection du texte lu dans la zone d'édition
            self.zone_texte.get_buffer().set_text(contenu_lu)
            self.label_info.set_text(f"Fichier ouvert avec succès : {gfile.get_basename()}")
        except Exception as e:
            # Gère proprement l'annulation par l'utilisateur ou une erreur d'accès
            self.label_info.set_text("Ouverture annulée ou erreur de lecture.")

    # --- ACTION : ENREGISTRER UN FICHIER ---
    @Gtk.Template.Callback()
    def on_bouton_enregistrer_clicked(self, button):
        dialog = Gtk.FileDialog.new()
        dialog.set_title("Enregistrer le fichier sous...")
        dialog.save(self, None, self.on_save_response)

    def on_save_response(self, dialog, result):
        try:
            gfile = dialog.save_finish(result)
            chemin_absolu = gfile.get_path()

            # Récupération du texte saisi par l'utilisateur dans le buffer
            buffer = self.zone_texte.get_buffer()
            texte_a_sauvegarder = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)

            # Écriture physique sur le disque dur avec Python
            with open(chemin_absolu, 'w', encoding='utf-8') as f:
                f.write(texte_a_sauvegarder)

            self.label_info.set_text(f"Fichier enregistré avec succès : {gfile.get_basename()}")
        except Exception as e:
            self.label_info.set_text("Enregistrement annulé ou erreur d'écriture.")

    # --- ACTION : STATISTIQUES ---
    @Gtk.Template.Callback()
    def on_bouton_action_clicked(self, button):
        buffer = self.zone_texte.get_buffer()
        texte_complet = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        nb_caracteres = len(texte_complet)
        nb_mots = len(texte_complet.split()) if texte_complet.strip() else 0
        self.label_info.set_text(f"Statistiques : {nb_mots} mots | {nb_caracteres} caractères")

