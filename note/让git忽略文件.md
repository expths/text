---
tags:
  - git
  - 配置
---
# .gitignore文件配置

配置 `.gitignore` 文件可以让 git 总是忽略一些文件。匹配的文件始终不会被跟踪，即使手动将其加入暂存区也会被阻止。

```console
The following paths are ignored by one of your .gitignore files:
[被忽略的文件]
hint: Use -f if you really want to add them.
hint: Turn this message off by running
hint: "git config advice.addIgnoredFile false"
```

## 配置文件代码格式

格式规范：

- 所有空行或者以 `#` 开头的行都会被 Git 忽略。
- 可以使用标准的 *glob* 模式匹配，它会递归地应用在整个工作区中。
- 匹配模式可以以`/`开头防止递归。
- 匹配模式可以以`/`结尾指定目录。
- 要忽略指定模式以外的文件或目录，可以在模式前加上叹号`!`取反。

代码关键字：

- 星号 `*` 匹配零个或多个任意字符。
- `[abc]` 匹配任何一个列在方括号中的字符。
- 问号 `?` 只匹配一个任意字符。
- 如果在方括号中使用短划线分隔两个字符，表示范围。
- 使用两个星号 `**` 表示匹配任意中间目录。

示例：

```gitignore
# 忽略所有的 .a 文件
*.a

# 但跟踪所有的 lib.a，即便你在前面忽略了 .a 文件
!lib.a

# 只忽略当前目录下的 TODO 文件，而不忽略 subdir/TODO
/TODO

# 忽略任何目录下名为 build 的文件夹
build/

# 忽略 doc/notes.txt，但不忽略 doc/server/arch.txt
doc/*.txt

# 忽略 doc/ 目录及其所有子目录下的 .pdf 文件
doc/**/*.pdf
```

## 子目录中可以拥有额外的配置文件

通常一个仓库可能只根目录下有一个 `.gitignore` 文件，它递归地应用到整个仓库中。但子目录下也可以有额外的 `.gitignore` 文件。子目录中的 `.gitignore` 文件中的规则只作用于它所在的目录中。
