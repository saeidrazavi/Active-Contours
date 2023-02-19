# Active Contours

In this repo, we implement active contours, in order to  stick to the desired object. we will say further how to implement it


<table>
  <tr>
    <td>Original image</td>
    <td>Active contour implementation</td>
  </tr>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/67091916/219969331-45cf7089-634c-4022-b761-9bc83db24390.jpg" width="400" height="250"/></td>
    <td><img src="https://user-images.githubusercontent.com/67091916/219969338-aa462fc1-989c-4be5-9562-211a97cb27a9.gif" width="400" height="250"/></td>

  </tr>
 </table>


## What is active contour?

Active contour is a type of segmentation technique which can be defined as use of energy forces and constraints for segregation of the pixels of interest from the image for further processing and analysis. Active contour described as active model for the process of segmentation

## Theory behind active contour

we have a contour and our goal is to minimize "energy" of this contour . this energy contains three section . 

$$E_{total}=E_{internals}+E_{external}$$


<br/>

$$E_{external}=\Sigma((G_{x}(x_{i},y_{i}))^{2}+(G_{y}(x_{i},y_{i}))^{2}$$

$$ where \ G_{x} \ is \ gradient \ of \ x \ axis \ and \ G_{y} \ is \ gradient \ of \ y \ axis $$$$

<br/>

$$E_{internal_{1}}=\Sigma({v_{i}-v_{i-1}}-d)^{2}$$

$$ where \ v_{i} \ is \ a \ tuple, \ consists \ of \ vertice \ coordinate. \ that \ is \ v_{i}=(x_{i},y_{i}) $$


we define $E_{internal_{1}}$ that is sensetive to distance from center of object . this parameter help us to make contour become closer to boarders. 
in order to avoid contour to pass object, we define another paramter that is senstive to gradian of image and as contour get closer, this paramter has bigger impact on it. this is beacuse avoiding contour pulled into object after reaching boarders . so we define :

$E_{internal_{2}}=\Sigma(\sqrt{\lvert{v_{i}-v_{center}}}^{2}\rvert-l)^{2}$ , where $l$ is the average distance between coordinates of vertices and center's coordinate

so to summarize our energy function is :

$E_{total}=\alpha_{0}\Sigma((G_{x}(x_{i},y_{i}))^{2}+(G_{y}(x_{i},y_{i}))^{2}+\alpha_{1}\Sigma(\left(\lvert{v_{i}-v_{i-1}}-d)^{2}\right\rvert)+\alpha_{2}\Sigma(\sqrt{\lvert{v_{i}-v_{center}}^{2}}\rvert-l)^{2}$

our task is to find minimum energy of snake. 
to find minimum energy we use dynamic programming (**viterbi algorithm**) : below we can see schematic of this algorithm:


<table>
  <tr>
    <td>Viterbi algorithm</td>
  </tr>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/67091916/219971059-71297ac6-e5f4-4f55-a6b3-d4922edcd469.PNG" alt="Drawing" style="width: 600px;"/> </td>
  </tr>
 </table>
 
 ##Preprocess data
 
  we use canny edge detection to calculate gradians of our image . after that i use two another method to remove background from forground :
 1) first we use guassin filter to remove noise from picture 
 2) use `filters.threshold_yen`. this filter is very strong method to remove background noise from forground

<table>
  <tr>
    <td>Canny edge detection</td>
    <td>Gaussian filter</td>
    <td>Yen threshold filter</td>
  </tr>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/67091916/219973682-e17ff56a-a0ef-425c-bf3e-8e50c8d99ae3.png" alt="Drawing" style="width: 600px;"/> </td>
    <td><img src="https://user-images.githubusercontent.com/67091916/219973683-cfe80a61-8d9d-4b6a-a082-7b20aecd9cd7.png" alt="Drawing" style="width: 600px;"/></td>
    <td><img src="https://user-images.githubusercontent.com/67091916/219973686-140c2961-799a-4858-8a2b-2096c42d491a.png" alt="Drawing" style="width: 600px;"/></td>
  </tr>
 </table>

## choose initial contour over object 
after choosing points all around the object , we determine initial contour(circular contour) . you can see the implementation of active contour in python file `active_contour.py`  

<table>
  <tr>
    <td>Initial contour</td>
    <td>Active contour </td>
  </tr>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/67091916/219973839-9a066408-d81c-4747-baba-1e23e988a388.png" width="400" height="250"/></td>
    <td><img src="https://user-images.githubusercontent.com/67091916/219969338-aa462fc1-989c-4be5-9562-211a97cb27a9.gif" width="400" height="250"/></td>

  </tr>
 </table>
