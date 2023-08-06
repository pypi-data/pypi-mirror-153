import io

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import seaborn_image as isns
import tensorflow as tf
from keras.callbacks import Callback


class ImageLogger(Callback):
    def __init__(self, log_dir, epoch_freq, num_images, class_names, sample_batch, phase):
        super().__init__()
        self.file_writer_image = tf.summary.create_file_writer(log_dir + f"/images_{phase}")
        self.test_images, self.test_masks = sample_batch
        self.test_images = self.test_images.numpy()
        self.test_masks = self.test_masks.numpy()

        self.test_images_ds = tf.data.Dataset.from_tensors(self.test_images).cache()
        options = tf.data.Options()
        options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.DATA
        self.test_images_ds = self.test_images_ds.with_options(options)

        self.class_names = class_names

        if not plt.colormaps.get("my_class_colors"):
            colors = sns.color_palette("colorblind", as_cmap=True)
            colors.insert(0, "#000000")  # BG black
            cmap = mpl.colors.ListedColormap(colors[: len(class_names)], name="my_class_colors")
            plt.colormaps.register(cmap)
        else:
            cmap = plt.colormaps.get("my_class_colors")
        self.bounds = [i for i in range(len(class_names) + 1)]
        self.bounds_mid = np.array(self.bounds)[1:] - 0.5
        self.norm = mpl.colors.BoundaryNorm(self.bounds, cmap.N)

        self.epoch_freq = epoch_freq
        self.num_images = num_images

    def plot_to_image(self, figure) -> tf.Tensor:
        """Converts the matplotlib plot specified by 'figure' to a PNG image and
        returns it. The supplied figure is closed and inaccessible after this call."""
        # Save the plot to a PNG in memory.
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        # Closing the figure prevents it from being displayed directly inside
        # the notebook.
        plt.close(figure)
        buf.seek(0)
        # Convert PNG buffer to TF image
        image = tf.image.decode_png(buf.getvalue(), channels=4)
        # Add the batch dimension
        image = tf.expand_dims(image, 0)
        return image

    def plot_image_grid(self, test_image, test_mask, test_pred) -> plt.Figure:
        f, axs = plt.subplots(
            nrows=1, ncols=4, gridspec_kw={"width_ratios": [1, 1, 1, 0.08], "wspace": 0.02}, figsize=(6, 2)
        )
        isns.imgplot(test_image, ax=axs[0], robust=True, cmap="gray", cbar=False, interpolation="nearest", origin="upper")
        axs[0].set_title("Image")

        isns.imgplot(test_mask, ax=axs[1], cmap="my_class_colors", cbar=False, interpolation="nearest", origin="upper")
        axs[1].set_title("Mask")

        isns.imgplot(test_pred, ax=axs[2], cmap="my_class_colors", cbar=False, interpolation="nearest", origin="upper")
        axs[2].set_title("Prediction")

        f.colorbar(
            mpl.cm.ScalarMappable(cmap="my_class_colors", norm=self.norm),
            ticks=self.bounds_mid,
            cax=axs[3],
            orientation="vertical",
        )
        axs[3].set_yticklabels(self.class_names)
        return f

    def on_epoch_end(self, epoch, logs=None):
        if (epoch % self.epoch_freq) == 0:
            # Use the model to predict the values from the validation dataset.
            test_pred_raw = self.model.predict(self.test_images_ds)
            if self.num_images > test_pred_raw.shape[0]:
                self.num_images = test_pred_raw.shape[0]

            for i in range(self.num_images):
                test_image = self.test_images[i].copy()
                # norm to 0,1
                test_image = (test_image - np.min(test_image)) * (1.0 / (np.max(test_image) - np.min(test_image)))

                test_mask = np.argmax(self.test_masks[i], axis=-1)
                test_pred = np.argmax(test_pred_raw[i], axis=-1)

                figure = self.plot_image_grid(test_image, test_mask, test_pred)
                grid_image = self.plot_to_image(figure)
                # Log figure as an image summary.
                with self.file_writer_image.as_default():
                    tf.summary.image(f"Example {i}", grid_image, step=epoch)
