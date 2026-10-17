# window.py
#
# Copyright 2026 Joao Batista
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

@Gtk.Template(resource_path='/com/github/batistajm/gtkText/window.ui')
class GtkTextWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'GtkTextWindow'

    zone_texte = Gtk.Template.Child()
    label_info = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        buffer = self.zone_texte.get_buffer()
        buffer.set_text("Bienvenue dans PyText !\nTapez votre texte ici.")

    # --- NOUVEAU : OUVRIR UN FICHIER ---
    @Gtk.Template.Callback()
    def on_bouton_ouvrir_clicked(self, button):
        dialog = Gtk.FileDialog.new()
        dialog.set_title("Ouvrir un fichier texte")
        # On lance la boîte de dialogue en lui passant la fenêtre actuelle (self)
        dialog.open(self, None, self.on_open_response)

    def on_open_response(self, dialog, result):
        try:
            gfile = dialog.open_finish(result)
            chemin_fichier = gfile.get_path()

            # Lecture du fichier avec Python
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()

            # Injection du contenu lu dans le buffer de texte
            self.zone_texte.get_buffer().set_text(contenu)
            self.label_info.set_text(f"Fichier ouvert : {gfile.get_basename()}")
        except Exception as e:
            # Gère l'annulation par l'utilisateur ou une erreur de lecture
            self.label_info.set_text("Ouverture annulée ou erreur de lecture.")

    # --- NOUVEAU : ENREGISTRER UN FICHIER ---
    @Gtk.Template.Callback()
    def on_bouton_enregistrer_clicked(self, button):
        dialog = Gtk.FileDialog.new()
        dialog.set_title("Enregistrer le fichier sous...")
        dialog.save(self, None, self.on_save_response)

    def on_save_response(self, dialog, result):
        try:
            gfile = dialog.save_finish(result)
            chemin_fichier = gfile.get_path()

            # Récupération du texte actuel dans le buffer
            buffer = self.zone_texte.get_buffer()
            texte_a_sauver = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)

            # Écriture du fichier avec Python
            with open(chemin_fichier, 'w', encoding='utf-8') as f:
                f.write(texte_a_sauver)

            self.label_info.set_text(f"Fichier enregistré : {gfile.get_basename()}")
        except Exception as e:
            self.label_info.set_text("Enregistrement annulé ou erreur d'écriture.")

    # --- STATISTIQUES (Étape précédente) ---
    @Gtk.Template.Callback()
    def on_bouton_action_clicked(self, button):
        buffer = self.zone_texte.get_buffer()
        texte_complet = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        nb_caracteres = len(texte_complet)
        nb_mots = len(texte_complet.split()) if texte_complet.strip() else 0
        self.label_info.set_text(f"Statistiques : {nb_mots} mots | {nb_caracteres} caractères")

