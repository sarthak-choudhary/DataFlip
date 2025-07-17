RQ2 runs DataFlip on every combination of target and injected tasks for a given backend LLM. The results are saved as JSON files and have the following structure:

```
{model_name} > The backend LLM. (e.g. claude-4-sonnet)
    |__target_{target_task}_inject_{injected_task}.json > target task and injected task for which we are running DataFlip (e.g. target_grammar_correction_inject_hate_detection.json)
            |__Benign Accuracy > Task accuracy on uncontaminated inputs
            |__ASV > Attack Success Value
            |__detect_rate > contaminated inputs detected by the detection LLM
            |__target_task_responses > Responses of the backend LLM on the target task data
            |__target_task > The target task
            |__injected_task_responses > Responses of the backend LLM on the injected task data (uncontaminated)
            |__injected_task > The injected task
            |__attack_responses > Responses of the backend LLM on contaminated inputs
            |__target_data > Data used for target_task_responses
            |__inject_data > Data used for injected_task_responses
            |__attacked_data > The inputs used for contaminating DataFlip
            |__detector_responses > Responses of the detection LLM on contaminated inputs
            |__detector_config > information about the detection LLM setup
            |__model_config > information about the backend LLM setup
```
