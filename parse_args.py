from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--exp_name", "-n",
        type=str, default="exp",
        help="Experiment name.")
    
    parser.add_argument(
        "--model_name", "-mn",
        type=str, default="EleutherAI/pythia-410m",
        help="Model name.")
    
    parser.add_argument(
        "--revision", "-r",
        type=str, default="step3000",
        help="Revision.")

    parser.add_argument(
        "--train_file", "-tf",
        type=str, default="train.gsv",
    )

    parser.add_argument(
        "--valid_file", "-vf",
        type=str, default="valid.gsv",
    )

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
        "--save_epoch", "-se",
        type=int, default=0,
        help="Save model every save_epoch epochs. 0 means no saving except final model.")

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

def parse_args_post():
    parser = ArgumentParser()
    parser.add_argument(
        "--answer_file", "-a",
        type=str, default=None,
        help="Answer file path.")
    
    parser.add_argument(
        "--result_file", "-r",
        type=str, default=None,
        help="Result file path.")
    
    parser.add_argument(
        "--file_dir", "-fd",
        type=str, default="raw_data/valid/dataset",
        help="File directory.")
    
    args = parser.parse_args()
    
    return args

def parse_args_infer():
    parser = ArgumentParser()
    parser.add_argument(
        "--model_dir", "-md",
        type=str, default=None,)
    
    parser.add_argument(
        "--output_dir", "-od",
        type=str, default=None,)
    
    parser.add_argument(
        "--infer_file", "-if",
        type=str, default=None,)
    
    args = parser.parse_args()
    
    return args

def parse_args_metrics():
    parser = ArgumentParser()
    parser.add_argument(
        "--label_file", "-l",
        type=str, default=None,
        help="label file path.")
    
    parser.add_argument(
        "--predict_file", "-p",
        type=str, default=None,
        help="predict file path.")
    
    args = parser.parse_args()
    
    return args