Client :
	Il doit être placé dans le dossier www/html du client robo.
	le fichier index et image/ dossier sont liés à la transmission vidéo, et je recommande de les changer (actuellement c'est très lent)
	les trois fichiers python sont pour le code qui doit toujours être exécuté (main_client appelle les autres fichiers)
		Il va exécuter 2 threads séparés, TCP et communication série.

Serveur :
	Il doit être placé dans le dossier www/html du client robo.
	Le dossier Static/ et Templates/ fait référence à Flask, un serveur python.
		Il a été choisi pour traiter les demandes qui seront faites sur les sites
	Le fichier qui devrait toujours être en cours d'exécution est le serveur principal (main_Server).

Arduino :
	Le fichier ControlSystem assure le contrôle de chaque moteur.
		Le contrôle du moteur avant et de la caméra se fait par position et non par vitesse.
	Le fichier principal est le MinuProjet_Arduino.