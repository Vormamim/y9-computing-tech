> For the complete documentation index, see [llms.txt](https://gosford-high-school.gitbook.io/9-computing-tech/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://gosford-high-school.gitbook.io/9-computing-tech/unit-2-mechatronics/2-representing-algorithms/representing-algorithms/further-examples.md).

# Further Examples

## Example

Whilst not for Raspberry Pi PICO, this is an example of what flowcharts and pseudocode could look like for a mechatronic / robotic system.

### Flowchart for One Subroutine and Mainline Routine

<figure><img src="https://1444032343-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F4gikgBQGRUb49XMCrCgU%2Fuploads%2F0ftFQoJ8WftXELCfFcZx%2Fimage.png?alt=media&amp;token=ed60d241-c479-4d69-83c4-2f4d9f89bf89" alt=""><figcaption></figcaption></figure>

### Pseudocode

```
BEGIN detect_object
    WHILE distance > 100mm
        READ distance
        Drive Forwards
    ENDWHILE
    Turn right 90 degrees
END detect_object


BEGIN
    detect_object
    collect_yellow
    detect_line
    collect_red
    drive_home
END
    
```
