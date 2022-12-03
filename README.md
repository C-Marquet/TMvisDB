# TMvis-DB

Welcome to **TMvis-DB**: A database to search and visualize predicted transmembrane proteins. :seal:

**TMvis-DB** provides per-residue transmembrane topology annotations for all proteins in [AlphaFold DB](http://example.com) (~ 200 million proteins, September '22) predicted as transmembrane proteins (~ 46 million). The annotations are predicted with [TMbed](http://example.com), and are visualized by overlaying them with [AlphaFold 2](https://www.nature.com/articles/s41586-021-03819-2) structures.

The web interface of **TMvis-DB** is implemented with [Streamlit](https://streamlit.io), and accessible here: https://tmvisdb.predictprotein.org.

----
#### Preview of TMvis-DB visualizations:

<img width="1200" alt="image" src="https://user-images.githubusercontent.com/73125710/202669572-5dffebee-73bd-4839-92b5-e3d2acdc20c1.png">
<details>
  <summary markdown="span"> <u><b>Figure caption</u></b> </summary>
  
**3D structure and membrane topology visualization protein DnaJ homolog subfamily C member 11 (Q9NVH1).** The protein DnaJ with (A) per-residue topology color-scheme: inside-to-outside TMH (light green), outside-to-inside TMH (dark green), inside-to-outside TMB (light blue), outside-to-inside TMB (dark blue), signal peptide (pink), other (grey), and (B) a per-residue AlphaFold color-scheme based on the confidence measure predicted local distance test (pLDDT): very low pLDDT ≤ 50 (red), low 50 < pLDDT ≤ 70 (yellow), confident 70 < pLDDT ≤ 90 (green), very confident pLDDT > 90 (blue). The predicted transmembrane topology aligns well with the predicted AlphaFold structure in regions of high pLDDT, and the length of the alpha-helix and beta-barrel could align with membrane boundaries.

</details>

----
#### :bulb: How to browse TMvis-DB:
To browse the 46 million predicted transmembrane proteins in TMvis-DB via a table, you can show a random selection or use the following filters:
- Transmembrane topology (alpha-helix, beta-strand)
- Include/Exclude sequences with predicted signal peptides
- Taxonomy (UniProt Organism Identifier, Domain, Kingdom)
- Protein length


#### :bulb: How to visualize predicted transmembrane proteins:
Single proteins of TMvis-DB can be selected for 3D-visualization of per-residue transmembrane topology annotation. You can either select a protein from the table you generated while browsing TMvis-DB, or you can directly enter a UniProt Identifier. The AlphaFold 2 structures of a protein is then shown with the corresponding color code of the predicted topology. You may also select the pLDDT score of AlphaFold 2 as a color code.

----
#### References:
- Preprint for TMvis-DB: [TMvis-DB](https://biorxiv.org/cgi/content/short/2022.11.30.518551)
- Structure predictions: [Alphafold DB](https://alphafold.ebi.ac.uk)
- Transmembrane topology predictions: [TMbed](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-022-04873-x)
- Visualization: [TMvis](https://github.com/Rostlab/TMvis)
- Protein-specific phenotype predictions: [LambdaPP](https://embed.predictprotein.org)
- Structural aligments: [Foldseek](https://search.foldseek.com/search)

#### Software:
- Website: [Streamlit](https://streamlit.io), [pandas](https://pandas.pydata.org)
- Database: [MongoDB](https://www.mongodb.com), [pymongo](https://github.com/mongodb/mongo-python-driver)
- 3D Visualization: [py3Dmol](https://3dmol.csb.pitt.edu), [stmol](https://github.com/napoles-uach/stmol)

#### Development & Maintenance:
- Corresponding Author: [Céline Marquet](https://github.com/C-Marquet)
- License: [License](https://license.com/)
- Resources & Maintenance: [Rostlab](https://rostlab.org)
