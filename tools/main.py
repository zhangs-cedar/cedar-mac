from cedar.init import *

img_origin = imread('tools/1.png',cv2.IMREAD_UNCHANGED)
print(img_origin.shape)
img = img_origin[:, :, 0]


# np在y方向找到第一个非0像素和最后一个非0像素
img_row = np.sum(img, axis=1)
row1 = np.where(img_row != 0)[0][0]
row2 = np.where(img_row != 0)[0][-1]
height = row2 - row1

# np在x方向找到第一个非0像素和最后一个非0像素
img_col = np.sum(img, axis=0)
col1 = np.where(img_col != 0)[0][0]
col2 = np.where(img_col != 0)[0][-1]
width = col2 - col1

padding = row1
img_cut = img_origin[row1-padding:row2+padding, col1-padding:col2+padding]

imwrite('tools/1_cut.png', img_cut)

imshow(img_cut)


plt.show()
