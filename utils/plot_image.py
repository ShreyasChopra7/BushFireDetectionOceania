import matplotlib.pyplot as plt

def plot(image, result):
    classes = result.shape[2] if len(result.shape) > 2 else 1
    fig, ax = plt.subplots(1, classes + 1)
    ax[0].set_title('Real Image')
    ax[0].imshow(image)
    if classes > 1:
        for i in range(classes):
            ax[i+1].set_title(f'Result (class {i+1})')
            ax[i+1].imshow(result[:, :, i])
    else:
        ax[1].set_title(f'Output')
        ax[1].imshow(result)
    plt.xticks([]), plt.yticks([])
    plt.show()
