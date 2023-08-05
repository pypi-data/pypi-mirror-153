# Package wizzi utils:  
## Installation: 
```bash
pip install wizzi_utils 
```
## Usage
```python
import wizzi_utils as wu # imports all that is available
print(wu.version()) 
```
* The above import will give you access to all functions and tests in wizzi_utils.<br/>
* Other than misc_tools, it is the user's responsibility to install the requirements to sub packages such
as torch, tensorflow and so on.
* For convenience, the wizzi_utils imports all it can from the sub packages, therefore
only the one import above is enough.
* Every function is covered by a test(usually the 'func_name'_test()). Use this to see how the 
function works and also to copy paste the signature.

###  misc_tools & misc_tools_test
'pip install wizzi_utils' made sure you'll have everything needed installed so they should be fully working,
so there is no namespace for misc_tools module(direct access from wu)<br/>
```python
import wizzi_utils as wu


def main():
    # all functions in misc_tools & misc_tools_test are imported to wizzi_utils
    print(wu.to_str(var=2, title='my_int'))  # notice only wu namespace

    # direct access to the misc_tools module
    print(wu.misc_tools.to_str(var=2, title='my_int'))  # not needed but possible

    wu.test.test_all()  # runs all tests in misc_tools_test.py
    wu.test.to_str_test()  # runs only to_str_test
    return


if __name__ == '__main__':
    wu.main_wrapper(
        main_function=main,
        seed=42,
        ipv4=True,
        cuda_off=False,
        torch_v=True,
        tf_v=True,
        cv2_v=True,
        with_profiler=False
    )
```

### All other packages
Other packages, e.g. torch_tools, will work only if you have all the dependencies written in the init file of the module
or by calling wu.wizzi_utils_requirements()

```python
import wizzi_utils as wu


def main():
    wu.wizzi_utils_requirements()  # will print all packages names and their requirements

    # access to a function in the torch module (must install torch and torchvision)
    print(wu.tt.to_str(var=3, title='my_int'))  # notice wu and tt namespaces. tt for torch tools

    # access to a function in the matplotlib module(must install matplotlib and mpl_toolkits)
    print(wu.pyplt.get_rgb_color(color_str='r'))

    # access to a module test
    wu.pyplt.test.test_all()  # all tests in pyplt module
    wu.pyplt.test.plot_3d_iterative_dashboard_test()  # specific test in pyplot module
    return


if __name__ == '__main__':
    wu.main_wrapper(
        main_function=main,
        seed=42,
        ipv4=True,
        cuda_off=False,
        torch_v=True,
        tf_v=True,
        cv2_v=True,
        with_profiler=False
    )
```  
### Examples:
```python
import wizzi_utils as wu


def main():
    # wu.wizzi_utils_requirements()
    return


if __name__ == '__main__':
    wu.main_wrapper(
        main_function=main,
        seed=42,
        ipv4=True,
        cuda_off=False,
        torch_v=True,
        tf_v=True,
        cv2_v=True,
        with_profiler=False
    )
```
```text
C:\Users\GiladEiniKbyLake\.conda\envs\wu\python.exe D:/workspace/2021wizzi_utils/temp/wu_test.py
--------------------------------------------------------------------------------
main_wrapper:
* Run started at 11-08-2021 15:02:30
* Python Version 3.6.8 |Anaconda, Inc.| (default, Feb 21 2019, 18:30:04) [MSC v.1916 64 bit (AMD64)]
* Operating System uname_result(system='Windows', node='Wizzi-Dorms', release='10', version='10.0.19041', machine='AMD64', processor='Intel64 Family 6 Model 158 Stepping 9, GenuineIntel')
* Interpreter: C:\Users\GiladEiniKbyLake\.conda\envs\wu\python.exe
* wizzi_utils Version 6.7.14
* Working Dir: D:\workspace\2021wizzi_utils\temp
* Computer Mac: 'deleted'
* CPU Info: AMD64, Intel64 Family 6 Model 158 Stepping 9, GenuineIntel, Physical cores 4, Total cores 8, Frequency 3601.00Mhz, CPU Usage 53.8%
* Physical Memory: C: Total 232.33 GB, Used 209.79 GB(90.30%), Free 22.55 GB, D: Total 931.39 GB, Used 530.3 GB(56.90%), Free 401.08 GB, E: PermissionError: [WinError 21] The device is not ready: 'E'
* RAM: Total 15.94 GB, Used 5.29 GB(33.2%), Available 10.65 GB 
* Computer ipv4: 'deleted'
* CUDA Version: v10.2 (cuDNN Version 7.6.5)
* PyTorch Version 1.9.0+cpu - GPU detected ? False
* OpenCv Version 4.5.3 - GPU detected ? False  # if built from source - this could be true
* TFLite Version 2.5.0
* Seed was initialized to 42
Function <function main at 0x000002184BAC1EA0> started:
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Total run time 0:00:00

Process finished with exit code 0
```
```python
import wizzi_utils as wu


def main():
    # mt package - main package
    wu.test.to_str_test()
    wu.test.add_color_test()
    wu.test.get_time_stamp_test()
    wu.test.get_time_stamp_test()
    wu.test.save_load_npz_test()
    wu.test.shuffle_np_arrays_test()
    wu.test.save_load_pkl_test()
    wu.test.nCk_test()
    wu.test.get_base_file_and_function_name_test()
    wu.test.file_or_folder_size_test()
    wu.test.classFPS_test()
    # pyplt package
    wu.pyplt.test.move_figure_by_str_test()
    wu.pyplt.test.plot_2d_many_figures_iterative_test()
    wu.pyplt.test.plot_3d_iterative_dashboard_test()
    wu.pyplt.test.compare_images_sets_test()
    wu.pyplt.test.compare_images_multi_sets_squeezed_test()  # if you have torch, torchvision
    # cvt package
    wu.cvt.test.move_cv_img_by_str_test()
    wu.cvt.test.unpack_list_imgs_to_big_image_test()
    # st package
    wu.st.test.download_file_test()    
    # tt package
    wu.tt.test.count_keys_test()
    wu.tt.test.to_str_test()
    wu.tt.test.save_load_tensor_test()
    wu.tt.test.OptimizerHandler_test()
    wu.tt.test.shuffle_tensors_test()
    wu.tt.test.count_keys_test()
    wu.tt.test.get_torch_version_test()
    wu.tt.test.save_load_model_test()
    wu.tt.test.model_summary_test()
    # models package
    wu.models.test.test_all()  # will download some models and do short tests
    # got package - first do the instructions
    wu.got.test.upload_delete_image_test()
    return


if __name__ == '__main__':
    wu.main_wrapper(
        main_function=main,
        seed=42,
        ipv4=True,
        cuda_off=False,
        torch_v=True,
        tf_v=True,
        cv2_v=True,
        with_profiler=False
    )
```     
    