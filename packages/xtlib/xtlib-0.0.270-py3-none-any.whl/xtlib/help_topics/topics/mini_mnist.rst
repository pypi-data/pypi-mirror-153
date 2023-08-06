.. _mini_mnist:

=======================================
MiniMnist Application 
=======================================

The miniMnist app:
  - is an ML training app used in the XT demo.
  - is based on the PyTorch MNIST sample app.
  - it trains on 60 samples (vs. of the normal 60,000 samples used in the normal MNIST task).
  - it is XT-enabled (logs hyperparameters and metrics to XT API)
  - it is Tensorboard-enabled (logs metrics to Tensorboard API
  - chosen for demo because its a real ML training task that is fast to train