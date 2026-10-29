> For the complete documentation index, see [llms.txt](https://gosford-high-school.gitbook.io/9-computing-tech/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://gosford-high-school.gitbook.io/9-computing-tech/unit-2-mechatronics/4-assessment-task-2/task-guide/algorithms.md).

# Algorithms

{% hint style="warning" %}

## **THREE ALGORITHMS**

You need to create **three algorithms** outlining your **proposed solution** using both **pseudocode and flowcharts.**&#x20;

These algorithms **WILL BE MARKED.**&#x20;

**For the purpose of THIS TASK, you may count EACH SUBROUTINE as a SEPARATE ALGORITHM (i.e. have one algorithm for your main routine (which uses the functions), then you can create subroutines for those functions used (define functions in Python).**
{% endhint %}

## Example

### Flowchart for One Subroutine and Mainline Routine

<figure><img src="https://1444032343-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F4gikgBQGRUb49XMCrCgU%2Fuploads%2FpwEutE7aebPK3A3EJ8yc%2Fimage.png?alt=media&amp;token=429692b8-ddc7-4348-839e-6d5106dd2781" alt=""><figcaption></figcaption></figure>

### Pseudocode

```
BEGIN too_hot()
    clear_outputs()
    OUTPUT red_Led.value(1)
    OUTPUT buzzer.on()
END too_hot


BEGIN
    WHILE true
        READ temp
        IF temp > 22 THEN
            too_hot()
        ELSE IF temp > 18 THEN
            just_right()
        ELSE 
            too_cold()
        ENDIF
    ENDWHILE
END  
```
