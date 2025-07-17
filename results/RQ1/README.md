RQ1 calculates extraction rates for a given detection LLM. The results are saved as JSON files and have the following structure:

1. `attacked_data`: list of contaminated prompts that will be appended to the detection instruction
2. `det_key_extraction`: instances where the detection LLM outputs the secret key and the signature word
3. `detect_rate`: instances where the detection LLM successfully detects the contaminated input
4. `detector_inputs`: list of contaminated inputs to the detection LLM
5. `detector_responses`: list of the detection LLM's responses 
6. `injected_task`: injected task name
7. `secret_keys`: list of secret keys used in detection instructions
8. `signature`: the signature word used
