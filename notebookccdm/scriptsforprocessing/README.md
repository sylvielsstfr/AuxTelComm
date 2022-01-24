# README.md

DM-Stack scripts usefull to process Holograms, Bias and Flats with DM



# production of bias with **biasConfig.py** :

         constructBias.py . --rerun dagoret_jan22_bias  @all_visitsbias/visitbias_2021-02-16_empty~empty.list  --batch-type none --configfile biasConfig.py --clobber-config  


# production of flats with **flatConfig.py**:

        constructFlat.py . --rerun dagoret_jan22_flats  @all_visitsflats/visitflat_2021-02-16_RG610~empty.list  --batch-type none --configfile flatConfig.py --clobber-config
  


# production of dispersed image with **processStar.py** :

- Spectractor has been decoupled from this version provided by Dominique (processConfig.py  , processStar.py)


        processStar.py . --rerun dagoret --configfile processConfig.py @visit.list



# remarks

- need to ingest Bias and Flats in DM-Stack


# OLD

Nouveau

Dominique Boutigny (he/him):montagne_enneigée:  15 h 41
@sylviedc J'ai modifié processStar.py pour débrancher spectractor Tu peux récupérer ma version da

ns: /sps/lsst/users/boutigny/AuxTel/repos/atmospec/python/lsst/atmospec/processStar.py 

(il suffit que tu remplaces le fichier processStar.py qui est dans ton répertoire atmospec par le mien).


 Ensuite il te faut copier /sps/lsst/users/boutigny/AuxTel/processConfig.py chez toi. La commande pour traiter une image est alors la suivante: processStar.py . --rerun dagoret --configfile processConfig.py --id dayObs='2021-07-07' seqNum=330  tu récupéreras alors l'image calexp dans: rerun/dagoret/calexp

Pour l'instant l'astrométrie se plante toujours sur cette image.
15 h 45
Pour traiter plusieurs images avec la même commande, tu peux créer un fichier visit.list contenant une ligne par image de la form
e --id dayObs='2021-07-07' seqNum=330
La commande à passer est alors: 

processStar.py . --rerun dagoret --configfile processConfig.py @visit.list (modifié) 

Dominique Boutigny (he/him):montagne_enneigée:  15 h 52
Petit détail supplémentaire, processCcd.py ne peut pas fonctionner tel quel sur les images "hologramme"
. C'est pour cette raison que les étapes isr , charImage et astrometry sont exécutées dans processStar.py (modifié) 


