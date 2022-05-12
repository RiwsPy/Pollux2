// leaflet.draw traduction
L.drawLocal = {
	draw: {
		toolbar: {
			actions: {
				title: "Quitter l'édition",
				text: 'Quitter'
			},
			finish: {
				title: "Finir l'édition",
				text: 'Finir'
			},
			undo: {
				title: 'Supprimer le dernier point dessiné',
				text: 'Supprimer le dernier point'
			},
			buttons: {
                polyline: 'Tracer une ligne',
                polygon: 'Dessiner un polygone',
                rectangle: 'Dessiner un rectangle',
                circle: 'Dessiner un cercle',
                marker: 'Placer un marqueur',
                circlemarker: 'Placer un cercle'
			}
		},
		handlers: {
			circle: {
				tooltip: {
					start: 'Cliquez et glissez pour dessiner le circle.'
				},
				radius: 'Rayon'
			},
			circlemarker: {
				tooltip: {
					start: 'Cliquez sur la carte pour placer le cercle.'
				}
			},
			marker: {
				tooltip: {
					start: 'Cliquez sur la carte pour placer le marqueur.'
				}
			},
			polygon: {
				tooltip: {
					start: 'Cliquez pour commencer à dessiner une forme.',
					cont: 'Cliquez pour continuer à dessiner une forme.',
					end: 'Cliquez sur le premier point pour terminer la forme.'
				}
			},
			polyline: {
				error: '<strong>Erreur :</strong> les lignes ne peuvent se chevaucher !',
				tooltip: {
					start: 'Cliquez pour commencer la ligne.',
					cont: 'Cliquez pour ajouter un point à la ligne.',
					end: 'Cliquez sur le dernier point pour terminer la ligne.'
				}
			},
			rectangle: {
				tooltip: {
					start: 'Cliquez et glissez pour dessiner un rectangle.'
				}
			},
			simpleshape: {
				tooltip: {
					end: 'Relâchez la souris pour terminer le dessin.'
				}
			}
		}
	},
	edit: {
		toolbar: {
			actions: {
				save: {
					title: 'Sauvegarder les changements',
					text: 'Sauvegarder'
				},
				cancel: {
					title: 'Quitter le mode suppression, annuler les changements',
					text: 'Annuler'
				},
				clearAll: {
					title: 'Retirer toutes les couches',
					text: 'Tout supprimer'
				}
			},
			buttons: {
				edit: 'Modifier une couche',
				editDisabled: 'Aucune couche à éditer',
				remove: 'Supprimer une couche',
				removeDisabled: 'Aucune couche à supprimer'
			}
		},
		handlers: {
			edit: {
				tooltip: {
					text: 'Faîtes glisser les points pour éditer les formes.',
					subtext: 'Cliquez sur Annuler pour revenir en arrière.'
				}
			},
			remove: {
				tooltip: {
					text: 'Cliquez sur une forme pour la supprimer.'
				}
			}
		}
	}
};

