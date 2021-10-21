## **Testing**

### **Notable Bugs Occurring During Development**
During the development phase of the site, I encountered a number of significant bugs while testing the output of my code. They were all mistakes which led to important lessons learned for future projects. These are documented below:

### **SSL Certificate Issue**
When initially connecting my project to my MongoDB database using **pymongo**, I was encountering an error which stated `[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed`. With the help of Tutor support, I discovered the solution to get around this issue was to add the string **“&ssl=true&ssl_cert_reqs=CERT_NONE”** to the end of my Mongo URI. The reason behind this issue was unfortunately beyond my understanding but I plan to further research it online after this project is completed.

 <img src="documents/testing/sig-err-3.png" alt="significant error 1" width="400"/> 

 <img src="documents/testing/sig-err-3-1.png" alt="significant error 1" width="400"/> 

### **Issues with Holiday Pros/Cons Data Submission to Backend**
When the `write_review` python function was first implemented, an issue occurred with how the holiday pros and cons were sent to the database. When a review was subsequently viewed by a user, the holiday pros and cons were appearing as separate individual letters of the first pro/con submitted. A visual of this is shown below:

<img src="documents/testing/sig-err-1.png" alt="significant error 1" width="250"/> 

This bug was caused by how the data was being retrieved from the `write_review.html` form. Originally I was using `list(request.form.get('holiday_pros'))` as my method to extract the data. After researching online, I adjusted this to `request.form.getlist('holiday_pros')` in order to correct the issue.

### **Cropped Headers in Review Cards**
In order to test the durability of the layout of the review cards on the **profile** page, I wrote a review of a location with a very long name (Llanfairpwllgwyngyll in Wales) in order to see how it would appear on the site. As expected, some of the elements of the review header would overflow when displayed on a phone screen, as shown below:

<img src="documents/testing/sig-err-2.png" alt="significant error 2" width="250"/> 

In order to manage this issue, I researched the bootstrap documentation and fopund a class called `text-truncate` which could be used to make the report appear in a more tidy fashion. The final appearance is below:

<img src="documents/testing/sig-err-2-sol.png" alt="significant error 2 solution" width="250"/>

### **User Feedback Bug Fixes**
In order to fully test the website, I shared it with family and friends in order to get feedback on how the site performed. Below are documented changes that were made that arose from the feedback I was given:

### **Charts Page Sorting**
Originally the sorting algorithm I used for some of the charts sorted solely on the average star rating or cost rating of the review. However this posed an issue. Countries/locations that had a high average score but a low number of reviews submitted were being displayed above countiries/locations which had the same average score but a higher number of submitted reviews. This is shown in the example below. Even though Japan and Ireland both had an average rating of 4 stars, Ireland had 4 reviews more than Japan. An average rating is more reliable if it is be calculated from a larger amount of data, Therefore Ireland should be displayed above Japan.

<img src="documents/testing/user-feed-fix-1-p.png" alt="cahrts page sorting issue" width="400"/>

In order to fix this issue, I added an extra sorting step in the function which sorted the countries/locations by review quantity and then by average score. This ensures that whenever two countries/locations were tied for average score, the country/location which had a higher number of submitted reviews displayed higher in the list.

### **User Form Validation**
For registering to the site, a regex pattern is used on the input fields on the **register** page form. This pattern allows only letters and numbers to be used for the username and password of the user. There is also a requirement that a minimum of 5 characters is used and a maximum of 15. If the user does not submit data which follows these requirements, I used bootstrap custom validation to display a message to the user to say the data was not valid. After testing with users, I got feedback that the message is too ambiguous and does not give a clear indication of what is needed to be valid. I adjusted this so that the requirments were clearer. Below can be seen the before and after of this adjustment.

<img src="documents/testing/user-feed-fix-2-p.png" alt="issue with validation" width="250"/>
<img src="documents/testing/user-feed-fix-2-s.png" alt="fix for issue with validation" width="245"/>

### **Login Function Error**
When testing the **login** page with users, I discovered that my login function was not correctly managing a situation where a user attempts to login with a username which passes client side validation but does not exist on the database. In order to correct this, I adjusted the code so that after the function initially extracts the username from the data, if the value returned is False (i.e. NoneType) then the function flashes a "Username not found!" message on the page.  
<img src="documents/testing/user-feed-fix-3-s.png" alt="username not found error" width="245"/>

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

* These were both linked and caused by human error. The unclosed `div` tag was corrected

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

<img src="documents/testing/html-val-register-e11.png" alt="html validator register html error 11" width="250"/>  

* This were both linked and caused by human error. The unclosed `div` tag was corrected

### **CSS Validator Results**
In order to validate the quality of my CSS Code, I passed it through the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/). No errors or warnings were found.

### **JavaScript Validator Results**
In order to validate the quality of my JavaScript Code, I passed it through the [Jshint linter](https://jshint.com/). No errors were found. Nine warnings ocurred for missing semicolons in bootstrap code that I used. I corrected these so the warnings do not appear.

### **Python Validator Results**
In order to validate the quality of my Python Code in `app.py`, I passed it through a [PEP8 online checker](https://pep8online.com//). [**Initial results**](documents/testing/python-val.png) showed 12 lines with **line too long (> 79 characters)** errors. I wnet through each affected line one by one and made adjustments in order to address these errors. The majority of cases were caused by the return statement for each of my functions. The `render_template` method I was returning as output took in alot of parameters which caused the line to exceed 79 characters. I could easily address these cases by breaking the line into multiple segments.

One case did appear which was slightly more difficult to correct. if was caused by some conditional logic. It is pictured below:

<img src="documents/testing/python-val-e0.png" alt="python validator error 1" width="400"/>  

The logic is neccessary for the subsequent calculations and I couldnt break the line into multiple segments. Therefore I chose to change the `review['location'].lower()` condition that was being checked to a variable called `rev_location`.

After these adjustments were made, I passed the new code thorugh the checker once more and got an ["**all right**"](documents/testing/python-val-final.png) result.

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

### **User Stories Validation**

**Site Viewer**
1. *I want to be able to create an account on HolidayHub*  
When the user first visits the site they are presented with a call to action panel on an index page. This panel contains a link to the **register** page of the site where the user has the ability to create an account. The user is prompted to create a username, a password and choose what type of holidays they normally enjoy. The holiday type determines their "traveller type" on their user profile statistics. For example, if the user chooses "cultural getaways" then they will be displayed as a "sophisticated tourist" traveller type on their profile. The user is also able to navigate to the **register** page via a link on the **login** page   
<img src="documents/testing/user-story-validation-sv-1.png" alt="logging out of the site" width="600"/> 

2. *I want to be able to log in to my account on HolidayHub*  
When the user first visits the site they are presented with a call to action panel on an index page. This panel contains a link to the **login** page of the site where the user has the ability to log into their previosuly created account. The user is also able to navigate to this page via a link on the **register** page    
<img src="documents/testing/user-story-validation-sv-2.png" alt="logging out of the site" width="400"/> 

3. *I want to be able to log out of my account on HolidayHub*  
Once logged in, the user can easily log out of the site by selecting the **Log Out** button that is visible in the navbar. Once they select this option, they will then be redirected to the **login** page of the site.  
<img src="documents/testing/user-story-validation-sv-3.png" alt="logging out of the site" width="400"/> 

4. *I want to be view my profile on HolidayHub*  
Once the user has registered on the site, they are immediately sent to their own personal **profile** page. They are also able to navigate back to this page by using the navbar at any point. On the **charts**,**read_review** and **edit_review** pages of the site, there is a button present which the user can use to redirect back to their personal profile. 

5. *I want to write a review on HolidayHub*  
The buttons to write a review is found in the users **profile** page, the **charts** page and the navbar of the site. When any of these buttons are pressed, the user is brought to a **write_review** page where there is a form present that they can fill out with their review.  
<img src="documents/testing/user-story-validation-sv-5.png" alt="writing a review on the site" width="400"/> 

6. *I want to edit a review on HolidayHub*  
This user story is satisfied when the user is viewing their **profile** page on the site. The page displays all reviews written by the user. There are three actionable buttons available for each review. One of these buttons is **Edit**. When the user clicks this button they can
<img src="documents/testing/user-story-validation-sv-6.png" alt="editing a review on the site" width="400"/> 

7. *I want to delete a review on HolidayHub*  
This user story is satisfied when the user is viewing their **profile** page on the site. The page displays all reviews written by the user. There are three actionable buttons available for each review. One of these buttons is **Delete**. The user can press this button if they choose to remove associated review from the site. Defensive programming is implemented via a warning modal which double checks with the user if they are certain that they want the particular review deleted.  
<img src="documents/testing/user-story-validation-sv-7.png" alt="defnsive programming on the site" width="400"/> 

8. *I want to see other users reviews on HolidayHub*  
This user story is satisfied when the user is navigating through the **charts** section of the site. In this page the user can select a location/country they want to see all user submitted reviews for. When chosen, they will then be brought to a **review** page which shows all reviews for that particular location.

9. *I want to see other users reviews by country on HolidayHub*  
When viewing the "Top Overall Rated Countries" chart that is located in the **charts** page of the site, the user can select a country to see all reviews submitted for the particular country.  
<img src="documents/testing/user-story-validation-sv-9.png" alt="navigation to other users' reviews on the site" width="400"/> 

10. *I want to see other users reviews by location on HolidayHub*  
When viewing the "Best Locations for Food" and the "Cheapest Reviews" charts that are located in the **charts** page of the site, the user can select a location to see all reviews submitted for the particular location.  
<img src="documents/testing/user-story-validation-sv-10.png" alt="navigation to reviews by location" width="400"/> 

11. *I want to see the best locations for food on HolidayHub*  
This story is satisfied on the **charts** page of the site. There is a chart titled "Best Locations for Food" which shows the best rated locations which had reviews that included food as one of the holiday pros. 

12. *I want to see the cheapest rated locations on HolidayHub*  
This story is satisfied on the **charts** page of the site. There is a chart titled "Cheapest Locations" which shows the cheapest rated locations based on the cost ratings of the locations reviews. 

13. *I want to see the best rated countries on HolidayHub*  
This story is satisfied on the **charts** page of the site. There is a chart titled "Top Overall Rated Countries" which shows the best rated countries based on their average review score. 

14. *I want the process of writing a review to be simple and intuitive*  
Writing a review is easily accessible from the users' profile page and navbar of the site. When writing all neccessary input fields are well structured and layed out. An intuitive slider system is used to enable the user to select the cost rating and review star rating of the location beign reviewed. Multiple elements can be selected when choosing the pros and cons of the holiday.

15. *I want the process of reading another users' review to be interesting and visually appealling*  
The appearance of other users reviews is both visually pleasant and insightful. The colorful elements used to show the pros, cons, cost rating and review score of the site are effective in that they catch the viewers eye while also conveying the most pertinent details of the review. The well structured comment section of the review allows the viewer to get more detailed information easily if they chose to read on.  
<img src="documents/testing/user-story-validation-sv-15.png" alt="appearance of read review on the site" width="300"/> 

16. *I want to view another person's profile on HolidayHub*  
This user story is satisfied when the user is navigating through the **charts** section of the site. In this page the user can select a location they want to see all reviews for. When chosen, they will then be brought to a **review** page which shows all reviews for that particular location. While looking at other peoples reviews, the user can choose to view their profile. they will then be brought to a **profile** page for that user, which details profile stats and all reviews written by that user.  
<img src="documents/testing/user-story-validation-sv-16.png" alt="navigation to a user profile on the site" width="700"/> 

**Site Owner**
1. *I want to provide unbiased, user driven travel advice*  
This user story is satisfied in the **charts** section of the site. This page aggregates all user reviews a provides charts which detail what the most well reviewed locations are. The charts are not determined by the owner of the site. User data will determine what appears in these charts.    
<img src="documents/testing/user-story-validation-so-1.png" alt="charts section of the site" width="400"/> 

2. *I want to create opportunities to generate revenue by promoting traffic to affiliate links accomodation booking sites*  
This story is satisfied on the **read_review** page of the site. A vibrant orange affiliate link button is visible below the heading of every review on the site. The button prompts the user towards booking a holiday for the location in the review on the affiliate's website. For the purpose of this assignment, a fake affiliate holiday booking website was created called "HolidayBook". The logo was designed using [canva](https://www.canva.com/)  
<img src="documents/testing/user-story-validation-so-2.png" alt="affiliate logo visible on read review page" width="400"/>  

### **Remaining Unfixed Bugs**

**Lowercase Usernames**  
When I first developed the register functionality in the site, I mistakenly used the python `.lower()` method to store all usernames in the database in lowercase. As a result a user might have registered with the name **"ADmIn"** on the site registration form but in the back end, the username was stored as **"admin"**. As I got deeper into the project, I started to encourage family and friends to test out using the site so that I could collect enough review data in order to improve how well the **charts** page appeared on the site. I had developed a small userbase on the site. Unfortunately only at this point I then realised that all of their usernames were stored in lowercase. In order for me to correct this issue, I could potentially lock some users out from the site. If it was changed so that uppercase characters were enabled, the existing usernames would need to be fixed by clarifying with each user whether or not they used uppercase characters when registering. In order to maintain the integrity of the site, I decided to keep this untouched. Lowercase usernames would be a unique aspect of the site which sets it apart from others.

**Holiday Pros/Cons Button Group Mobile Behaviour**  
For the holiday pros and cons selection on the review forms of the site, I used a Bootstrap [checkbox button group component.](https://getbootstrap.com/docs/5.1/components/button-group/#checkbox-and-radio-button-groups) When testing this on a mobile phone, I found it had very unpredictable behaviour. In particular when a user wants to uncheck a particular item, the component is not very intuitive. This particular issue did not occur on desktop devices. I believe the issue is caused by the change in the display of the component when being viewed on a smaller screen. Unfortunately I ran out of time to fix this particular issue. The component is still functional however and during user testing this issue was never brought up.

**Redirect Back to Login Page after Logging In**  
When the user logs in, it is possible for them the press the back button on their browser and get redirected back to the log in page. This log in page should not be reachable once the user has logged in. To fix this issue for a future release, I would implement logic in the back end to redirect the user to their profile page if the session already has a logged in user.

**Misleading Charts**  
In the **charts** page, the user can view a chart called "Best Locations for Food". Each location has a count of reviews which shows the number of reviews which have food labelled as a pro for that particular location. The user can then select the location to see all reviews for that particular location. They are then redirected to a page where they can see **all** reviews for that particular location. This is slightly misleading because the user might expect to be seeing only reviews with **food** for that location e.g. the review count might show **"Reviews: 1"** (meaning there was one food review) however 5 reviews appear on the **reviews** page, 4 of which didnt include food. This is not neccessarily a major bug but would be good to address in a future update.