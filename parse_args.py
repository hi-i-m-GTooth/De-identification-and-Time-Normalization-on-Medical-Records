from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "exp_name", "-n",
        type=str, default="exp",
        help="Experiment name.")
    
    parser.add_argument(
        "--subdataset_size", 
        type=int, default=20000, 
        help="Number of samples in each subdataset.")
    
    parser.add_argument(
        "--batch_size", "-b",
        type=int, default=8,
        help="Batch size.")
    
    parser.add_argument(
        "--epoch", "-e",
        type=int, default=3,
        help="Epoch.")

    parser.add_argument(
        "--lr",
        type=float, default=3e-5,
        help="Learning rate.")
    
    parser.add_argument(
        "--device", "-d",
        type=str, default="cuda:1",
        help="Device.")
    
    args = parser.parse_args()
    
    return args

