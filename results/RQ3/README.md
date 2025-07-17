RQ3 calculates FPRs and FNRs for the base and finetuned detection LLM. The results are saved as JSON files:
1. `detector_benign_prompts.json`: Results for FPR on benign inputs
2. `detector_combined_attack_prompts.json`: Results for FNR on contaminated inputs crafted using the combined attack
3. `detector_dataflip_prompts.json`: Results for FNR on contaminated inputs crafted using DataFlip.

They have the following structure:

```
{injected_task} > the injected task of contaminated input (or the target task when calculating FPRs for benign inputs. e.g. summarization)
    |__{target_task} > the target task of the backend LLM, considered while crafting contaminated inputs (not present for benign inputs. e.g. hate_detection).
        |__det_base > base model (Mistral 7B) performance
        |       |__det_rate > detection rate using det_base, corresponds to FPRs or FNRs
        |       |__responses > Responses of det_base to benign or contaminated inputs.
        |
        |__det_ft >  finetuned model (DataSentinel) performance
                |__det_rate > detection rate using det_ft, corresponds to FPRs or FNRs
                |__responses > Responses of det_ft to benign or contaminated inputs.
```