def set_jurkat_configs(args):
    args.batch_size = 256
    args.fixmatch_k_img = 8192
    args.simclr_batch_size = 1024
    args.labeled_ratio_start = 0.025
    args.labeled_ratio_stop = 0.225
    args.add_labeled_ratio = 0.025
    args.merged = False
    args.autoencoder_z_dim = 128

    return args
