set -x
cd ../../alphapose
CONFIG=${1:-"./configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml"}
CKPT=${2:-"./pretrained_models/fast_res50_256x192.pth"}
VIDEO=${3:-"../server1/SM/media/img"}
OUTDIR=${4:-"../server1/SM/output"}
python ./scripts/demo_inference.py \
    --cfg ${CONFIG} \
    --checkpoint ${CKPT} \
    --indir ${VIDEO} \
    --outdir ${OUTDIR} \
    --save_img --pose_track --detbatch 1 --posebatch 30 --format open
# args = '--cfg ./configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml --checkpoint ./pretrained_models/fast_res50_256x192.pth --indir ./examples/demo --outdir ./examples/result --save_img --pose_track --detbatch 1 --posebatch 30 --format open'
        # args = args.split()
sleep 10s