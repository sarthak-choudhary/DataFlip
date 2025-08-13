# DataFlip
Recent defenses based on known-answer detection (KAD) have achieved near-perfect performance by using an LLM to classify inputs as clean or contaminated. We present [DataFlip](https://arxiv.org/abs/2507.05630), an adaptive attack that consistently evades KAD defenses with detection rates as low as 0.5% while reliably inducing malicious behavior with success rates of up to 93%, without needing white-box access to the LLM or any optimization procedures. This repo can be used for replicating our experiments and builds on top of the [Open Prompt Injection](https://github.com/liu00222/Open-Prompt-Injection).

![Overview of KAD. Part (1) illustrates KAD under benign input, where the detection LLM follows the detection instruction and returns the secret key—correctly classifying the input as \texttt{Clean}.
Part (2) shows KAD under a basic attack, where the detection LLM follows the injected instruction and returns an adversarial output—correctly classifying the input as \texttt{Contaminated}.
Part (3) presents KAD under our adaptive attack (DataFlip), where the detection LLM follows the \texttt{IF} clause of the injected instruction to return the secret key—causing KAD to misclassify the input as \texttt{Clean} and allowing it to bypass detection.](data/dataflip_workflow.png)

## Updates
* (07/23/25): We include a preprocessing step to convert all contaminated inputs to the detection LLM to lowercase and restrict the detection LLM's output to 10 tokens. We also provide a new prompt template for DataFlip that achieves perfect evasion rates on several tasks while significantly improving ASVs.

## Setup
### Packages and Environment
Pre-requisite: [conda](https://www.anaconda.com/docs/getting-started/miniconda/install)

Install the environment using the following command: 
```
conda env create -f environment.yml --name my_custom_env
```
Then activate the environment:
```
conda activate my_custom_env
```
### Models
Finetuned DataSentinel models can be downloaded from the [Open Prompt Injection repo](https://github.com/liu00222/Open-Prompt-Injection). We use `detector_large` for our experiments.

### Experiments
1. **RQ1: Secret Key Extraction.** We show in `RQ1.ipynb` that DataFlip can extract the secret key contained within the detection instruction at an average rate of 94%, with no prior knowledge of the key. 
2. **RQ2: Attacking Strong KAD.** We demonstrate the effectiveness of DataFlip in `RQ2.ipynb`, where we consistently evade a detection LLM finetuned using DataSentinel, while reliably getting the backend LLM to follow the injected instruction, with success rates upto 93%.
3. **RQ3: Fine-tuned vs Base FNR.** We compare the FNR of a detector fine-tuned using DataSentinel with an instruction fine-tuned Mistral 7B model in `RQ3.ipynb`. We find that it shows essentially no improvement on samples crafted using existing attacks, while underperforming by up to 83% on DataFlip crafted samples.

### Important Files
You can find our implementation of DataFlip here: `OpenPromptInjection/attackers/DataFilpAttacker.py`

### Parsing Results
All our results are available in `results`, under the corresponding experiment title (`RQ1, RQ2, RQ3`). We provide a guide to parse result files in separate READMEs in each result folder.
___

## Citation

If you use our code useful, kindly cite the following paper:

```
@misc{choudhary2025detectpromptinjectionsllm,
      title={How Not to Detect Prompt Injections with an LLM}, 
      author={Sarthak Choudhary and Divyam Anshumaan and Nils Palumbo and Somesh Jha},
      year={2025},
      eprint={2507.05630},
      archivePrefix={arXiv},
      primaryClass={cs.CR},
      url={https://arxiv.org/abs/2507.05630}, 
}
```
