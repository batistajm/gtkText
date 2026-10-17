import subprocess  # Indispensable pour lancer le script externe .sh
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

@Gtk.Template(resource_path='/com/github/batistajm/gtkText/window.ui')
class GtktextWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'GtktextWindow'

    # Liaison des widgets définis dans le XML
    zone_texte = Gtk.Template.Child()
    label_info = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        buffer = self.zone_texte.get_buffer()
        buffer.set_text("Bienvenue dans PyText !\nTapez ou ouvrez un fichier texte.")

    # --- 1. OUVRIR UN FICHIER ---
    @Gtk.Template.Callback()
    def on_bouton_ouvrir_clicked(self, button):
        dialog = Gtk.FileDialog.new()
        dialog.set_title("Ouvrir un fichier texte")
        dialog.open(self, None, self.on_open_response)

    def on_open_response(self, dialog, result):
        try:
            gfile = dialog.open_finish(result)
            chemin_absolu = gfile.get_path()
            with open(chemin_absolu, 'r', encoding='utf-8') as f:
                contenu_lu = f.read()
            self.zone_texte.get_buffer().set_text(contenu_lu)
            self.label_info.set_text(f"Fichier ouvert : {gfile.get_basename()}")
        except Exception:
            self.label_info.set_text("Ouverture annulée ou erreur de lecture.")

    # --- 2. ENREGISTRER UN FICHIER ---
    @Gtk.Template.Callback()
    def on_bouton_enregistrer_clicked(self, button):
        dialog = Gtk.FileDialog.new()
        dialog.set_title("Enregistrer le fichier sous...")
        dialog.save(self, None, self.on_save_response)

    def on_save_response(self, dialog, result):
        try:
            gfile = dialog.save_finish(result)
            chemin_absolu = gfile.get_path()
            buffer = self.zone_texte.get_buffer()
            texte_a_sauvegarder = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
            with open(chemin_absolu, 'w', encoding='utf-8') as f:
                f.write(texte_a_sauvegarder)
            self.label_info.set_text(f"Fichier enregistré : {gfile.get_basename()}")
        except Exception:
            self.label_info.set_text("Enregistrement annulé ou erreur d'écriture.")

    # --- 3. EXÉCUTER LE SCRIPT BASH (Bouton Analyser) ---
    @Gtk.Template.Callback()
    def on_bouton_action_clicked(self, button):
        buffer = self.zone_texte.get_buffer()
        texte_complet = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)

        # /!\ Pensez à vérifier que ce chemin vers votre script traitement.sh est bien le bon
        chemin_script = "/home/joao/Desktop/xProg/Python/Apprentissage_GTK4/gtkText/traitement.sh"

        try:
            statut_execution = subprocess.run(
                [chemin_script, texte_complet],
                capture_output=True,
                text=True,
                check=True
            )
            message_bash = statut_execution.stdout.strip()
            self.label_info.set_text(message_bash)
        except subprocess.CalledProcessError:
            self.label_info.set_text("Erreur lors de l'exécution du script Bash.")
        except Exception:
            self.label_info.set_text("Script introuvable ou droits manquants.")

