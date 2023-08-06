# conan-conan

This was created in an assignment.

DOI: 

The goal of this project is to visualize international tourism expenses of countries.

Using a dataset, conan-conan can visualize international tourism of up to four countries.

The dataset is downloadable from:

https://api.worldbank.org/v2/en/indicator/ST.INT.RCPT.CD?downloadformat=excel

The number of the vertical axis indicates the US dollars in millions.

![Figure_1conan_Japan](https://user-images.githubusercontent.com/103731249/171558533-ea57dbcf-de1b-4ce0-bdcc-fb7d27504834.png)

# How to install conan-conan on Linux, MacOS, or WSL on Windows

You may need matplotlib library.

$ pip install matplotlib

$ pip install conan-conan

# ow to install conan-conan if you have a trouble

$ pip install conan-conan --force-reinstall --no-cache-dir --no-binary :all:

# How to run conan-conan

The following command can display international tourism of Canada.

$ conan-conan Canada

![Figure_1conan_Canada](https://user-images.githubusercontent.com/103731249/171560020-d6fe68ee-4c42-40f6-a465-31b32ea1f23f.png)

The following command can display conan spending of Japan and Canada.

$ milspend Japan Canada

![Figure_1conan_JananCanada](https://user-images.githubusercontent.com/103731249/171561550-3fabf65b-1622-4fad-aa50-550a2b3d4488.png)


