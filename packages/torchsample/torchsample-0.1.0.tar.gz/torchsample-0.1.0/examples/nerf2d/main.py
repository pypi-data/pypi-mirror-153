import argparse
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, IterableDataset
from torchvision import transforms
from tqdm import tqdm

import torchsample as ts

transform = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ]
)


class SingleImageDataset(IterableDataset):
    def __init__(self, fn, batch_size):
        self.image = cv2.cvtColor(cv2.imread(str(fn)), cv2.COLOR_BGR2RGB)
        self.image = transform(self.image)  # (3, h, w)
        self.batch_size = batch_size
        self.size = self.image.shape[-1], self.image.shape[-2]  # (x, y)

    def __iter__(self):
        while True:
            out = {}
            out["coords"] = ts.coord.randint(0, self.batch_size, self.size)
            out["rgb"] = ts.sample.nobatch(out["coords"], self.image, mode="nearest")
            yield out


def main():
    parser = argparse.ArgumentParser(
        description="NeRF 2D Example.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("input/polite.jpg"),
        help="Input image to learn.",
    )
    parser.add_argument(
        "--batch-size", type=int, default=16384, help="Number of samples per minibatch."
    )
    parser.add_argument("--lr", type=float, default=3e-4, help="AdamW learning rate.")
    parser.add_argument(
        "--iterations",
        type=int,
        default=int(2e3),
        help="Number of training iterations.",
    )
    parser.add_argument(
        "--save-freq",
        type=int,
        default=200,
        help="Every this many training iterations, perform a full query "
        "and save the prediction.",
    )
    parser.add_argument(
        "--pos-enc", action="store_true", help="Use gamma positional encoding."
    )
    args = parser.parse_args()

    output_folder = Path("output") / f"{args.input.stem}_pos-enc={args.pos_enc}"
    output_folder.mkdir(parents=True, exist_ok=True)

    if args.pos_enc:
        mlp_in = 40
    else:
        mlp_in = 2
    model = ts.models.MLP(mlp_in, 256, 256, 256, 3)

    dataset = SingleImageDataset(args.input, args.batch_size)
    dataloader = DataLoader(dataset, batch_size=1, num_workers=0)

    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)

    print("Begin Training")
    pbar = tqdm(zip(range(args.iterations), dataloader))

    for iteration, batch in pbar:
        optimizer.zero_grad()
        # TODO: pos enc
        coords = batch["coords"]
        if args.pos_enc:
            coords = ts.encoding.gamma(coords)
        pred = model(coords)

        loss = F.l1_loss(pred, batch["rgb"])

        pbar.set_description(f"loss: {loss:.3f}")

        loss.backward()
        optimizer.step()

        if (iteration + 1) % args.save_freq == 0 or iteration == args.iterations - 1:
            coords = ts.coord.full_like.nobatch(dataset.image)

            if args.pos_enc:
                coords = ts.encoding.gamma(coords)

            with torch.no_grad():
                raster = model(coords)
                raster = raster.numpy()

            # Undo the normalization
            raster = (raster * 0.5) + 0.5
            raster = np.clip((raster * 255).round(), 0, 255).astype(np.uint8)
            out_fn = output_folder / f"{iteration + 1}.jpg"
            cv2.imwrite(str(out_fn), cv2.cvtColor(raster, cv2.COLOR_RGB2BGR))


if __name__ == "__main__":
    main()
