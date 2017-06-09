#!/bin/bash


origin=`git config remote.origin.url`
base=`dirname "$origin"`/`basename "$origin" .git`

# Output LaTeX table in chronological order
echo "\\begin{tabular}{l l l l}\\textbf{Detail} & \\textbf{Author} & \\textbf{Description} & \\textbf{Date}\\\\\\hline"
git log --pretty=format:"\\href{$base/commit/%H}{%h} & %an & %s & %ad\\\\\\hline" --after="2017-05-23"
echo "\end{tabular}" 
