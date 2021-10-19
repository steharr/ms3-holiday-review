## **Testing**

### **Notable Bugs Occurring During Development**
During the development phase of the site, I encountered a number of significant bugs while testing the output of my code. They were all mistakes which led to important lessons learned for future projects. These are documented below:

### **Issues with Holiday Pros/Cons Data Submission to Backend**
When the `write_review` python function was first implemented, an issue occurred with how the holiday pros and cons were sent to the database. When a review was subsequently viewed by a user, the holiday pros and cons were appearing as separate individual letters of the first pro/con submitted. A visual of this is shown below:

<img src="documents/testing/sig-err-1.png" alt="significant error 1" width="250"/> 

This bug was caused by how the data was being retrieved from the `write_review.html` form. Originally I was using `list(request.form.get('holiday_pros'))` as my method to extract the data. After researching online, I adjusted this to `request.form.getlist('holiday_pros')` in order to correct the issue.

### **Cropped Headers in Review Cards**
In order to test the durability of the layout of the review cards on the **profile** page, I wrote a review of a location with a very long name (Llanfairpwllgwyngyll in Wales) in order to see how it would appear on the site. As expected, some of the elements of the review header would overflow when displayed on a phone screen, as shown below:

<img src="documents/testing/sig-err-2.png" alt="significant error 2" width="250"/> 

In order to manage this issue, I researched the bootstrap documentation and fopund a class called `text-truncate` which could be used to make the report appear in a more tidy fashion. The final appearance is below:

<img src="documents/testing/sig-err-2-sol.png" alt="significant error 2 solution" width="250"/>

### **HTML Validator Results**
In order to validate the quality of my HTML Code, I passed it through the [W3C HTML Validator](https://validator.w3.org/) for all pages of my site to ensure there were no major issues. As there is Jinja templating code throughout the html pages, source code was taken from the rendered pages and passed into the validator (Rather than passing it a URL). Below are the results:

`index.html`  
No errors or warnings

`register.html`  
Two errors:
  
<img src="documents/testing/html-val-register-e1.png" alt="html validator register.html error 1" width="300"/>

* This was a typo mistake

<img src="documents/testing/html-val-register-e2.png" alt="html validator register.html error 1" width="300"/>

* This was a mistake made when customizing a bootstrap component for the select element of the register form. It was corrected by changing the `aria-describedby` attribute to point to the label for the username input field

`login.html`  
No errors or warnings

`profile.html`  
No errors or warnings

`read_review.html`  
Three errors:

<img src="documents/testing/html-val-register-e3.png" alt="html validator register.html error 3" width="250"/>

* This was human error mistake, corrected by removing

<img src="documents/testing/html-val-register-e4.png" alt="html validator register.html error 4" width="300"/>  

<img src="documents/testing/html-val-register-e5.png" alt="html validator register.html error 5" width="390"/>

* This were both linked and caused by human error. The unclosed `div` tag was corrected

`write_review.html`   
Five errors & 1 warning:

<img src="documents/testing/html-val-register-e6.png" alt="html validator register.html error 6" width="400"/>  

* These were both linked to the **cost** rating slider which the user can adjust. The reason for the "pattern" error is a human error mistake, this was corrected by removing. The reason for the attribute "required" error was intentional, I wanted to ensure the user selects a value for this field. Since this is not allowed, I removed it and kept the min value of the field equal to 1, so that something is always submitted to the back end.

<img src="documents/testing/html-val-register-e7.png" alt="html validator register.html error 7" width="400"/>  

* This duplicate declaration was caused by human error, corrected by removing the id from both elements

<img src="documents/testing/html-val-register-e8.png" alt="html validator register.html error 8" width="400"/>  

* These were both linked to the **review** rating slider which the user can adjust. The reason for the "pattern" error is a human error mistake, this was corrected by removing. The reason for the attribute "required" error was intentional, I wanted to ensure the user selects a value for this field. Since this is not allowed, I removed it and kept the min value of the field equal to 1, so that something is always submitted to the back end.

`edit_review.html`  
2 errors:

<img src="documents/testing/html-val-register-e9.png" alt="html validator register.html error 9" width="400"/>  

* This was accidentally caused by duplicate options in the select element for "Holiday Type" containing the **selected** attribute. This was corrected by removing the incorrectly added attribute.

<img src="documents/testing/html-val-register-e10.png" alt="html validator register.html error 10" width="250"/>  

* This was a typo mistake

`charts.html`  
84 errors:

* These errors were caused by multiple stray end tags for `span` elements in the lowest costs chart. They were cloned multiple times because of the amount of currency elements on the page when it is generated. They were easily corrected in the template. the page was passed through the validator again and came out with no errors

`reviews.html`  
2 errors:

<img src="documents/testing/html-val-register-e11.png" alt="html validator register.html error 11" width="250"/>  

* This were both linked and caused by human error. The unclosed `div` tag was corrected

### **CSS Validator Results**
In order to validate the quality of my CSS Code, I passed it through the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/). No errors or warnings were found.

### **JavaScript Validator Results**
In order to validate the quality of my JavaScript Code, I passed it through the [Jshint linter](https://jshint.com/). No erros were found. Nine warnings ocurred for missing semicolons in bootstrap code that I used. I corrected these so the warnings do not appear.

### **Python Validator Results**
In order to validate the quality of my Python Code in `app.py`, I passed it through a [PEP8 online checker](https://pep8online.com//). [Initial results](documents/testing/python-val.png) showed 12 lines with **line too long (> 79 characters)** errors. I wnet through each affected line one by one and made adjustments in order to address these errors. The majority of cases were caused by the return statement for each of my functions. The `render_template` method I was returning as output took in alot of parameters which caused the line to exceed 79 characters. I could easily address these cases by breaking the line into multiple segments.

One case did appear which was slightly more difficult to correct. if was caused by some conditional logic. It is pictured below:

<img src="documents/testing/python-val-e0.png" alt="python validator error 1" width="400"/>  

The logic is neccessary for the subsequent calculations and I couldnt break the line into multiple segments. Therefore I chose the  `review['location'].lower()` condition that was being checked to a variable called `rev_location`.

After these adjustments were made, I passed the new code thorugh the checker once more and got an [**all right**](documents/testing/python-val-final.png) result.

### Lighthouse Performance Results
In order to assess the performance of my site I ran a lighthouse review on both the mobile and desktop versions of each page in the site. Below are the results:

`index.html` 
* Mobile:  
<img src="documents/testing/lighthouse-index-mobile.png" alt="lighthouse mobile report results for index page" width="300"/> 

* Desktop:  
<img src="documents/testing/lighthouse-index-desktop.png" alt="lighthouse desktop report results for index page" width="300"/> 

`register.html` 
* Mobile:  
<img src="documents/testing/lighthouse-register-mobile.png" alt="lighthouse mobile report results for register page" width="300"/> 

* Desktop:  
<img src="documents/testing/lighthouse-register-desktop.png" alt="lighthouse desktop report results for register page" width="300"/> 

`login.html`
* Mobile:  
<img src="documents/testing/lighthouse-login-mobile.png" alt="lighthouse mobile report results for login page" width="300"/> 

* Desktop:  
<img src="documents/testing/lighthouse-login-desktop.png" alt="lighthouse desktop report results for login page" width="300"/> 

`profile.html`
* Mobile:  
<img src="documents/testing/lighthouse-profile-mobile.png" alt="lighthouse mobile report results for profile page" width="300"/> 

* Desktop:  
<img src="documents/testing/lighthouse-profile-desktop.png" alt="lighthouse desktop report results for profile page" width="300"/> 

`read_review.html`
* Mobile:  
<img src="documents/testing/lighthouse-readreview-mobile.png" alt="lighthouse mobile report results for readreview page" width="300"/> 

* Desktop:  
<img src="documents/testing/lighthouse-readreview-desktop.png" alt="lighthouse desktop report results for readreview page" width="300"/>  

`write_review.html`
* Mobile:  
<img src="documents/testing/lighthouse-writereview-mobile.png" alt="lighthouse mobile report results for writereview page" width="300"/> 

* Desktop:  
<img src="documents/testing/lighthouse-writereview-desktop.png" alt="lighthouse desktop report results for writereview page" width="300"/>  

`edit_review.html`  
* Mobile:  
<img src="documents/testing/lighthouse-editreview-mobile.png" alt="lighthouse mobile report results for editreview page" width="300"/> 

* Desktop:  
<img src="documents/testing/lighthouse-editreview-desktop.png" alt="lighthouse desktop report results for editreview page" width="300"/>  

`charts.html`
* Mobile:  
<img src="documents/testing/lighthouse-charts-mobile.png" alt="lighthouse mobile report results for charts page" width="300"/> 

* Desktop:  
<img src="documents/testing/lighthouse-charts-desktop.png" alt="lighthouse desktop report results for charts page" width="300"/>  

`reviews.html`
* Mobile:  
<img src="documents/testing/lighthouse-review-mobile.png" alt="lighthouse mobile report results for review page" width="300"/> 

* Desktop:  
<img src="documents/testing/lighthouse-review-desktop.png" alt="lighthouse desktop report results for review page" width="300"/>  

### User Stories Validation

### Remaining Unfixed Bugs