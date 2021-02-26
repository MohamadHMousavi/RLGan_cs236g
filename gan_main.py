from torch.backends import cudnn

import argparse
import sys
import torch
from gan_trainer import Trainer
from Losses import ChamferLoss
from visualizer import Visualizer


def str2bool(v):
    return v.lower() in ('true')


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--data_path', metavar='DIR', default='GFV_data', help='Path to Complete Point Cloud Data Set')

    parser.add_argument('-s', '--split_value', default=0.9, help='Ratio of train and test data split')

    parser.add_argument('--pretrained_path', default='')

    # Model hyper-parameters
    parser.add_argument('--max_action', type=float, default=10)

    parser.add_argument('--adv_loss', default='wgan-gp', type=str, choices=['wgan-gp', 'hinge'])  #
    parser.add_argument('--l_size', default=32, type=int)
    parser.add_argument('--g_num', type=int, default=5)
    parser.add_argument('--z_dim', type=int, default=1)
    parser.add_argument('--g_conv_dim', type=int, default=64)
    parser.add_argument('--d_conv_dim', type=int, default=64)
    parser.add_argument('--lambda_gp', type=float, default=10, help='gradient penalty')

    # GPU settings
    parser.add_argument('--gpu_id', type=int, default=0, help='gpu ids: e.g. 0, 1. -1 is no GPU')

    # Visualizer Settings
    parser.add_argument('--name', type=str, default='GFV',
                        help='name of the experiment. It decides where to store samples and models')
    parser.add_argument('--display_winsize', type=int, default=256, help='display window size')
    parser.add_argument('--display_id', type=int, default=2000, help='window id of the web display')
    parser.add_argument('--port_id', type=int, default=8099, help='Port id for browser')
    parser.add_argument('--print_freq', type=int, default=10, help='Print Frequency')

    # Training setting
    parser.add_argument('--total_step', type=int, default=1000000, help='how many times to update the generator')
    parser.add_argument('--d_iters', type=float, default=5)
    parser.add_argument('--batch_size', default=50, type=int)
    parser.add_argument('--num_workers', type=int, default=2)
    parser.add_argument('--g_lr', type=float, default=0.0001)
    parser.add_argument('--d_lr', type=float, default=0.0001)
    parser.add_argument('--lr_decay', type=float, default=0.0)
    parser.add_argument('--beta1', type=float, default=0.5)
    parser.add_argument('--beta2', type=float, default=0.9)

    # using pretrained
    parser.add_argument('--pretrained_num', type=int, default=None)

    # Misc
    parser.add_argument('--train', type=str2bool, default=True)
    parser.add_argument('--parallel', type=str2bool, default=False)
    # parser.add_argument('--use_tensorboard', type=str2bool, default=False)

    # Path
    parser.add_argument('--log_path', type=str, default='./logs')
    parser.add_argument('--model_save_path', type=str, default='./models')
    parser.add_argument('--sample_path', type=str, default='./samples')
    parser.add_argument('--attn_path', type=str, default='./attn')

    # Step size
    parser.add_argument('--log_step', type=int, default=100)
    parser.add_argument('--sample_step', type=int, default=100)
    parser.add_argument('--model_save_step', type=float, default=10.0)

    return parser.parse_args(args)


if __name__ == "__main__":
    args = sys.argv[1:]
    args = parse_args(args)

    """ GPU training """
    cudnn.benchmark = True
    args.device = torch.device(
        "cuda:%d" % args.gpu_id if torch.cuda.is_available() else "cpu")
    torch.cuda.set_device(args.gpu_id)

    # TODO: add latent_loader
    latent_loader = []

    # only used for visualization
    model_decoder = []

    chamfer = ChamferLoss(args)

    """ Visualization """
    visualizer = Visualizer(args)

    args.display_id = args.display_id + 10
    args.name = 'Validation'
    vis_Valid = Visualizer(args)
    vis_Valida = []
    args.display_id = args.display_id + 10

    for i in range(1, 12):
        vis_Valida.append(Visualizer(args))
        args.display_id = args.display_id + 10

    if args.train:
        trainer = Trainer(None, args, latent_loader, model_decoder, chamfer)
        trainer.train()
    else:
        # TODO: add tester
        print('not implemented')
        # tester = Tester(data_loader.loader(), args, valid_loader)
        # tester.test()
