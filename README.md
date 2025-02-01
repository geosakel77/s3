# 📘 **Implementation of Relevance and Actionability Quality Metrics for CTI**

*This project is the implementation and experimental testing of the relevance and actionability metrics using
probabilistic data structures and algorithms.*

---

## **Table of Contents**

1. [Introduction](#introduction)  
2. [Objectives](#objectives)  
3. [Background and Theory](#background-and-theory)  
4. [Methodology](#methodology)  
5. [Results](#results)  
6. [Conclusion and Future Work](#conclusion-and-future-work)  
7. [Dependencies](#dependencies)  
8. [Usage](#usage)  
9. [Contributing](#contributing)  
10. [Acknowledgments](#acknowledgments)  
11. [License](#license)  

---

## **Introduction**

S3 is the technical implementation of two Cyber Threat Intelligence (CTI) quality metrics as those proposed in a paper under development. 
The goal is to present how those metrics can be implemented and  measured by utilizing existing ontologies, and knowledge bases. 

---

## **Objectives**

- To develop the proposed architecture for the metric measurement.  
- To implement the mechanisms that measures the metrics. 
- To execute a number of experiments in hypothetical organizations.

---

## **Background and Theory**

### Relevant Theory
The relevant theory involved in the implementation of this project are related to:
- CTI.   
- Probabilistic algorithms and data structures.  
- CTI quality metrics

### Literature Review
This project leverages previous work on CTI systems modeling and CTI quality metrics development.

---

## **Methodology**

The methodology followed for the calculation of the Relevance metric is described in the following image:
![Relevance Metric Calculation](images\\relevance_generic_algorithm.png)

The methodology followed for the calculation of the Actionability metric is described in the following image:
![Actionability Metric Calculation](https://github.com/geosakel77/s3/blob/master-1/images/actionability_generic_algorithm.png)


### Experimental Workflow
1. **Data Collection**:  
   - CTI Products Sources: 
     - [MITRE ATT&CK](https://attack.mitre.org/) 
     - [CISA KNOWN VULNERABILITIES](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
     - [CVE](https://www.cve.org/)
     - [ALIENVAULT](https://otx.alienvault.com/dashboard/new)
     - [FEEDLY](https://feedly.com/i)
     - [MALPEDIA](https://malpedia.caad.fkie.fraunhofer.de/)
     - [MISP FEEDS](https://www.misp-project.org/feeds/)
     - [MITRE ATLAS](https://atlas.mitre.org/)
     - [TWEETFEED](https://tweetfeed.live/)
     - [MANDIANT](https://www.mandiant.com/)
   - Ontologies & Datasets: 
     - [Big Picture Companies](https://docs.bigpicture.io/docs/free-datasets/companies/)
     - [FIBO](https://spec.edmcouncil.org/fibo/)
     - [NACE](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Statistical_classification_of_economic_activities_in_the_European_Community_(NACE))
     - [DIT](https://rrdg.centr.org/projects/standards/domain-industry-taxonomy/)
     - [GPO](https://data.ontocommons.linkeddata.es/vocabulary/GeneralProcessOntology(gpo))
     - [CPE](https://nvd.nist.gov/products/cpe)
     - [PTO](http://www.productontology.org/)
     - [ECCF](https://op.europa.eu/en/web/eu-vocabularies/dataset/-/resource?uri=http://publications.europa.eu/resource/dataset/54i)
   - Datasets Statistics

| Num. of CTI products in dataset | Num. of CTI products in validation dataset | 
|---------------------------------|--------------------------------------------|
| 32012                           | 5000                                       |

2. **Preprocessing**: Typical text preprocessing techniques has been applied for the preparation of the data.   
3. **Modeling/Experiments**: Provide technical details (e.g., equations, algorithms, tools):
    - Models tested with key parameters.
    - Computational frameworks or hardware setup (e.g., HPC systems).

### Tools and Software
- Software Environment: Python, MATLAB, R, etc.  
- Libraries/Frameworks: TensorFlow, PyTorch, NumPy, etc.  

---

## **Results**

Summarize the key findings of the research/work in a methodical manner. Include visualizations if possible.

- **Quantitative Results**: Numerical summaries, tables, or performance metrics.  
- **Graphs/Figures**: Provide plots, diagrams, or key figures to support the results.

Example:
| Experiment         | Metric A | Metric B |  
|--------------------|----------|----------|  
| Test Case 1        | 92.4%    | 0.874    |  
| Test Case 2        | 88.1%    | 0.812    |

---

## **Conclusion and Future Work**

Conclude the findings and propose follow-up research directions.

- **Summary**: Recap the main results and their implications.  
- **Future Work**: Outline limitations and suggestions for improvement.  

Example:  
While the proposed model achieves [result], further work is required to [future goal]. Extending this work to [new application] is a priority for future research.

---

## **Dependencies**

- Language: Python (>= 3.8)  
- Libraries: annotated-types (0.7.0), antlr4-python3-runtime (4.9), anyio (4.4.0), appdirs (1.4.4), arrow (1.3.0), attrs (24.2.0), beautifulsoup4 (4.13.0b2), 
bitarray (2.9.2), cachetools (5.5.0), cattrs (24.1.0), certifi (2024.8.30), charset-normalizer (3.3.2), click (8.1.7), colorama (0.4.6), colour (0.1.5), contourpy (1.3.1),
cpe (1.3.0), cybox (2.1.0.21), cycler (0.12.1), datasketch (1.6.5), datefinder (0.7.3), deepdiff (8.0.1), defusedxml (0.7.1), Deprecated (1.2.14), deprecation (2.1.0), 
distro (1.9.0), drawsvg (2.4.0), et-xmlfile (1.1.0), filigran-sseclient (1.0.1), fonttools (4.55.2), fpdf2 (2.8.1), fqdn (1.5.1), h11 (0.14.0), httpcore (1.0.5),
httpx (0.27.2), idna (3.8), importlib_metadata (8.4.0), isodate (0.6.1), isoduration (20.11.0), jiter (0.5.0), joblib (1.4.2), jsonpointer (3.0.0), jsonschema (4.23.0),
jsonschema-specifications (2023.12.1), kiwisolver (1.4.7), loguru (0.7.2), lxml (5.3.0), maec (4.1.0.17), mandiant_ti_client (local), Markdown (3.7), markdown-it-py (3.0.0), 
matplotlib (3.9.3), mdurl (0.1.2), mitreattack-python (3.0.6), mixbox (1.0.5), mmh3 (4.1.0), netaddr (1.3.0), nltk (3.9.1), numpy (2.1.1), openai (1.44.0), openpyxl (3.2.0b1),
opentelemetry-api (1.27.0), opentelemetry-sdk (1.27.0), opentelemetry-semantic-conventions (0.48b0), ordered-set (4.1.0), orderly-set (5.2.2), owlready2 (0.46), packaging (24.1),
pandas (2.2.2), pika (1.3.2), pika-stubs (0.1.3), pillow (10.4.0), platformdirs (4.2.2), pluralizer (1.2.0), pooch (1.8.2), prometheus_client (0.20.0), pycountry (24.6.1), 
pycti (6.2.18), pydantic (2.9.0), pydantic_core (2.23.2), Pygments (2.18.0), pyparsing (3.1.4), PyPDF2 (3.0.1), pyprobables (0.6.0), pyrsistent (0.20.0), python-dateutil (2.9.0.post0), 
python-json-logger (2.0.7), python-magic-bin (0.4.14), pytz (2024.1), PyYAML (6.0.2), rdflib (7.0.0), referencing (0.35.1), regex (2024.7.24), requests (2.28.2), 
requests-cache (1.2.1), responses (0.21.0), rfc3339-validator (0.1.4), rfc3986-validator (0.1.1), rich (13.8.0), rpds-py (0.20.0), scalable-cuckoo-filter (1.1), scipy (1.14.1), 
seaborn (0.13.2), shellingham (1.5.4), simplejson (3.19.3), six (1.16.0), sniffio (1.3.1), soupsieve (2.6), stix (1.2.0.11), stix2 (3.0.1), stix2-elevator (4.1.7), 
stix2-patterns (2.0.0), stix2-validator (3.2.0), stixmarx (1.0.8), tabulate (0.9.0), taxii2-client (2.3.0), tenacity (9.0.0), tqdm (4.66.5), treelib (1.7.0), typer (0.12.5), 
types-python-dateutil (2.9.0.20240821), typing_extensions (4.12.2), tzdata (2024.1), uri-template (1.3.0), url-normalize (1.4.3), urllib3 (1.26.20), weakrefmethod (1.0.3), 
webcolors (24.8.0), win32-setctime (1.1.0), wrapt (1.16.0), XlsxWriter (3.2.0), zipp (3.20.1),  
- OS: Ubuntu 24.04, Windows 11  

---

## **Usage**

- Run setup.py 
- Run main.py

### Installation
1. Clone the repository:  
   ```bash
   git clone https://github.com/username/project-name.git
   cd project-name