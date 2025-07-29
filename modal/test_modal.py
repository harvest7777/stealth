import modal

def test_training():
    f = modal.Function.from_name("lerobot-finetune-app", "run_lerobot_a100")

    future = f.remote(
        dataset_repo_id="danaaubakirova/koch_test",
        model_id="lerobot/pi0",
        policy_name="modal_pi0_test",
        save_freq=100000,
        log_freq=5,
        steps=20
    )
    print(future)
if __name__ == "__main__":
    # Example job ID for testing
    test_job_id = "40280c63-5653-453f-a9bc-e4ab156ab7b0"
    
    # Run tests
    test_training()