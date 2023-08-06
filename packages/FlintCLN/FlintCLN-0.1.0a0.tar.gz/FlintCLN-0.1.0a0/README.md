FlintCLN is a Python-based linter for ensuring readability, reproducibility and standards for Computational Lab Notebooks.


## Introduction

A great challenge of any research program  is ensuring reproducibility of results and continuity of research projects as individuals come and go in the research program. Often, a scientist will maintain a [lab notebook](https://www.training.nih.gov/assets/Lab_Notebook_508_(new).pdf) that records all aspects of their experimental work. This record is meant to help others understand the tasks the researcher performed, the protocols used, and results.  If properly maintained, the lab notebook should guide anyone in reproducing results.  The lab notebook serves as a reference to the researcher when writing the Methods section of published manuscripts showcasing results.

Often data analysis is a necessary part of many experiments. Yet, it is not clear, however, how to preserve a record of computational analyses in a lab notebook such that others can easily reproduce results. The following are examples where challenges exist:

- A researcher can organize directories in ways that are not intuitive and  are only understandable by them.
- Similarly, input data files, intermediate data files and result file names may not be intuitive.
- Multiple analyses may be housed in the same directory making it difficult to know which files belong to a given analysis.
- In a UNIX environment, exact command-lines used to execute programs, retrieve or wrangle data may be missing making it impossible for anyone else to know exact parameters or arguments were used.

To help alleviate this problem, the Ficklin Computational Biology program at Washington State University has developed a set of standards for organizing computational lab notebooks in a UNIX environment. The standard is designed to help ensure reproducibility of results, readability of all work by others in the team, and near real-time access to results by anyone in the team.  A description of the standard is provided below.  This software is used to help check a computational lab notebook to ensure that standards are met. This style of checking is known as "linting". The software is the Ficklin Lab Linter for Computational Lab Notebooks (FlintCLN).  

This standard for computational lab notebooks is provided in the hopes that it may be useful for other groups.  

## How to Use FlintCLN

### Installation
To use FlintCLN first install it using the following:

```bash
    pip install FlintCLN
```

### Linting your Project
To check that a project repository meets the CLN standard, run FlinCLN in the following way:

```bash
flint-cln --project_dir <project dir>
```

Where `<project dir>` is the path to the directory where your project is housed.  A list of errors and warnings will be printed to the terminal.  Make fixes to any errors and re-run the tool as many times as needed.

## Do you want to Contribute?
This standard and linting tool are not perfect, yet it is offered in the hopes that it may be useful to others to help foster greater readability, reproducibility and consistency when computational analyses are required for a research project. If you would like to offer suggestions to improve the standard please submit an issue to the issue queue to initiate discussion.

## The Standard
### Guiding Principles

A computational lab notebook standard should provide a way to ensure reproducibilty, readability and continuity of a computational project. It should also support flexibility and creativity.  The guidelines listed below should help ensure the former while supporting the latter. But it is up to you to make sure that any lab notebook is readable and reproducible.  

This standard makes use of [Git](https://git-scm.com/), [README markdown](https://www.markdownguide.org/basic-syntax/) and a formal directory structure as described below.

### Versioning

This standard has a version number.  As changes to the standard are made, the version number is incremented.  As new versions of this standard are developed, the FlintCLN tool will be backwards compatible such that it will be able to lint the current and older versions of the standard.

### The CL Notebook -- Version 0.1

The Computational Lab Notebook (CLN) should be organized around a single project. Therefore, a researcher may contribute to multiple lab notebooks.

The CLN should contain written notes about the project, documents, input data, command-line instructions, computational scripts (e.g., R, Python, Matlab, etc.), computational notebooks (e.g. Jupyter Notebooks), intermediate files, results and reports.

The CLN should be usable by multiple researchers simultaneously.  Often multiple individuals contribute to a single project.  Their computational tasks and results should all be visible to others in the project, and one researcher may perform an analysis results created by another in the same notebook.

### Creating a CLN

The [Git](https://git-scm.com/) tool is used by software developers for version control and simultaneous development from multiple distributed individuals.  It maintains a history of all changes made in the software by all individuals, and anyone with access to the software's git repository can see the current state of the software.   To support a CLN, this standard proposes using Git.  The WC3 consortium provides a [tutorial for learning Git](https://www.w3schools.com/git/).

To create a new CLN you can uses free online services such as [GitHub](https://github.com/) or [GitLab](https://gitlab.com/). These services offer both public and private repositories. Follow the instructions on either of these platforms to create a new repository for a new CLN.  

Once a CLN is created, it can be cloned on any machine such as a laptop, UNIX workstation, or high-performance cluster.  As a researcher adds content to the CLN they can "push"  updates to the online server.  Other team members can "pull" recent changes and see them on their own machines.


### Terminology
The following terms are used by this standard:

- **Analysis**: Execution of a program or development of scripts to analyze data and generate new results for exploration.
- **Task**:  A task is any individual "unit" of analysis.
- **Task Collection**:  A task collection is a group of tasks.
- **Workflow**: A set of tasks that must be completed in a specific order within a project.

### The CLN Base Directory
Each CLN will have a base or "root" directory.  All tasks and task collections will be housed in this directory and its sub directories.  

The base directory must have directories with the following names:

| Directory Name | Purpose |
| -------------- | ------- |
| `00-docs` | Stores all documentation about the project such as emails, meeting notes, publications, presentations, etc. |
| `01-input_data` |  Stores all input data, that is not reproducible. |

The following directories are recommended but not required:

| Directory Name | Purpose |
| -------------- | ------- |
| `00-reports` | Stores files that were provided to collaborators for reporting progress. Each separate report should have a separate folder. The folder should have the date as the prefix to the directory in the form YYYY-MM-DD indicating the date the report was delivered to the collaborator. |
| `00-pubs` |  Stores files or links to files that are used in publications. |

### Tasks and Task Collections
A **task** is an individual "unit" of analysis. The researcher or research team will decide what these "units" are.  For example, consider a research project that includes Differential Gene Expression (DEG) analysis.  Such an analysis will require the following steps:

1.  Retrieve input transcript sequence data (e.g. RNA-seq).
2.  Retrieve whole genome data files.
3.  Perform gene or transcript quantification using ore more more alignment or pseudoalignment tools.
4.  Perform quality checks on count data (e.g. PCA analysis, outlier detection, normalization)
5.  Perform differential gene expression analysis.  

This set of steps is an informal **workflow** that the researcher must follow in order.

All of these steps could be performed in a single directory on the computer, however this may limit flexibility and overwhelm the researcher with too many files in one folder.  Instead, each of the steps above could be divided into separate "tasks" with a corresponding directory.  

For example, steps 1 and 2 retrieve input data that is not reproducible by this project so according to the instructions in the "The CLN Base Directory" section that data goes into the `01-input_data`.   Steps 3, 4 and 5 could go into separate directories named appropriately for each step.  For example:

| Directory Name | Purpose |
| -------------- | ------- |
| `02-create_GEM` | Stores the work that quantifies gene expression from the RNA-seq data (i.e., creates the gene expression matrix (GEM)) |
| `03-analyze_GEM` | Stores the work for quality checks on the GEM (e.g., PCA analysis, outlier removal, normalization, etc.) |
| `04-DEG_analysis` | Stores the work for DEG analysis. |

Notice that each directory has a two-digit numeric prefix (e.g., `01-`, `02-`, `03-`, etc.).  This prefix provides the order that these tasks should be executed.

A good rule-of-thumb is to create a task directory for steps that can be repeated using different tools or different parameter sets.  For example, there may be several tools to perform the same task. For this example, for quantification of gene expression data, some tools are [Hisat2](http://daehwankimlab.github.io/hisat2/), [Salmon](https://salmon.readthedocs.io/en/latest/salmon.html), [Kallisto](https://pachterlab.github.io/kallisto/about) and [STAR](https://github.com/alexdobin/STAR).  Perhaps there is interest to try multiple tools to compare results and afterwards decide which performs best.  Sub directories can be created to support this.  For example, sub directories for each tool could be created in the following way:

| Directory Name | Purpose |
| -------------- | ------- |
| `02-create_GEM/01-Hisat2` | Stores the Hisast2 tool run |
| `02-create_GEM/02-STAR` | Stores the STAR tool run|
| `02-create_GEM/03-Kallisto` | Stores the kallisto tool run |
| `02-create_GEM/04-Salmon` | Stores the Salmon tool run |

Such a group of tasks in a single directory is a **task collection**.

By separating the **workflow** into separate tasks, and using sub directories to organize different attempts at the same task, researchers can:

- Pick-and-chose the best results to use in later steps.
- Maintain a history of all attempts at a task.
- Keep different attempts at a task in separate folders.

Task directories and task collections should follow these rules:

1. A **task** and **task collection** directory should always have a numeric prefix followed by a dash (e.g. `01-`, `02-`, `03-`, etc.)
2. The numeric prefixes should be sequential and in the order that each task should be performed.  
3. The numeric prefixes must not skip or duplicate numbers. They must be sequential.
4. The first **task** in a **task collection** should start with the prefix `01-`
5. The researcher can provide any name for the **task** after the numeric prefix.
6. Each **task** and **task collection** directory must have a `README.md` file to describe to someone else the purpose and contents of the directory. See the "`README.md` files" section below for specifications.
7. A **task collection** should only contain task directories and the `README.md` file and no other files.
8. A **task** directory can have any number of files and subdirectories specific to the analysis.

Some notes:
- All of the tasks required by a project may not be known at the time the project is created. Often the researcher creates tasks and task collections as needed.
- The researcher may rename the task directories at any time.  It may be determined that a new analysis is needed but it needs to occur in between two existing tasks.  The numbering can be changed to insert the new analysis.

- Task names should be short and descriptive. The ideal task name is one that will help the researcher and other team members recognize what analysis is performed in the directory.


### README.md files.
To help ensure readability of the CLN, all directories (base, task collections and tasks) will have a `README.md` file. This `README.md` file should be written in [README markdown](https://www.markdownguide.org/basic-syntax/) format.  It's purpose is to describe to another team member the purpose of the project (i.e., workflow), task collection or task to someone else.

#### The README.md in the Base Directory
The README.md file in the base directory should have the following sections:

| Section Header | Section Content |
| ------ | ------- |
| `##Project Overview` |  This section provides a brief overview of the purpose of the project. It can give a brief description of the steps that are performed in the project workflow. |
| `##Project Contributors` |  Indicate the names of individuals who worked on the project and specify what their contributes were |
| `##Directory Structure` | Lists each task or task collection directory  that resides in the base directory and briefly describes its purpose |

#### The README.md in Task and Task Collection Directories.
Every **task** and **task collection** directory should contain a `README.md` file that should have the following sections:

| Section Header | Section Content |
| ------ | ------- |
| `##Directory Overview` |  Provide a brief description for the purpose of the directory |
| `##Directory Structure` |  Provides a brief description of each file and sub directory in the directory.

### Directory Suffixes
Often, a researcher will try an analysis and disregard it as not useful, or explore a tool to see how it works.  Such tasks are important in the **workflow** but may not be meaningful for other team members who may be looking at the project later on.  A researcher can mark **task** or **task collection** directories as "deprecated" or "experimental" respectively. A deprecated directory is one where the analysis was performed but was deemed unneeded or not useful for the project but is kept for historical purposes.  An experimental directory is one in which the researcher wants to keep a history of exploratory testing but other team members need not look there for results.

For example, in the DEG analysis workflow described above, if 4 different alignment tools (e.g., Hisat2, Kallisto, Salmon and STAR) were performed but the results from one of those will be used and the others can be marked as deprecated.

The following suffixes are supported:

| Suffix | Purpose |
| ------ | ------- |
| `-DEPRECATED` | Use this suffix for directories where the analysis was completed but is no longer being used. The files should follow all of the protocols described in this document and be fully reproducible.  But, files in such directories *should not* be used for other downstream analyses unless those directories are also marked as deprecated. |
| `-EXPERIMENTAL` |  Use this for tasks that are temporary or exploratory.  Files in such directories *should not* be used for other downstream analyses. |
| `-FROZEN` |  Use this for a task whose results have or will be used in a publication.  A directory that is frozen should have no other edits, changes or updates to ensure reproducibility.|


### Methods.md Files
Often, steps performed in a **task** require commands be executed in the UNIX terminal shell. Examples may be data retrieval/download (e.g., via `wget` commands), renaming files, data wrangling (with tools like `awk`, `sed`, `grep`, etc.), BASH scripting, or submission of task to a high-performance compute cluster.  If such commands are used in an analysis, the commands should be cut-and-pasted from the terminal, exactly as they were executed, into the the `Methods.md` file.  This file should use the README markdown format which is convenient to integrate notes and code into the same document.  

Researchers should be careful to copy all commands executed and provide sufficient documentation for each to help someone else understand exactly why those commands were executed.  Remember every **task** should be reproducible so this file is critical when the command-line is used.  

### Jupyter Notebooks
Jupyter Notebooks are a convenient way to integrate descriptive comments, code, figures, data tables and results into a single document. Use of such notebooks helps improve the reproducibilty of any analysis.

Here are some tips for including such notebooks in your **task* directory:

- If you use a Jupyter notebook be sure to describe it in the README.md file and indicate the order in which they should be executed.
- While it is not required, if you have multiple notebooks, you can give them numeric prefixes like the **task** directories to indicate the order they should be executed.
- Always keep in mind the notebook is not just for you, it is also for those who come after you who might want to use your work or learn from what you have done.  Be verbose and make sure you keep the "other" reader in mind as you work in the notebook.
    - If you are confused by a tool or parameters then odds are someone else will be too.  Document your confusion and the answers you found.
    - Always state why you are doing a particular task or function call
    - Remember to write down what you learned or decisions you made from the work that was done in a notebook.
    - Document pitfalls and failures as well.   
- Be sure that the sequence of cells follows a thought process (i.e. don't jump around in the notebook).
- Avoid reusing the same variable name to store refactored data frames. Because if someone re-runs a cell they may get different results.

### R or Python Scripts
If you work directly with R, Python or other language and develop stand-alone scripts or programs,  be sure to:

- Intersperse your code with comments to help others fully understand what each block of code is doing.  
- Always describe the scripts in the README.md file and indicate when they should be used in order to reproduce results.

### Referring to Data Files
The CLN should be fully self-contained. Your methods, notebooks and scripts should never refer to files outside of the project directories. When referring to data files in **task** directories, always use a path relative to the current **task** directory you are on.  For example, if you are in a task directory in the base directory and need to refer to data in the `01-input_data` directory use a relative path such as `../01-input_data/my_data_file.txt`.

This is critical as it ensures that anyone who clones the repository on their own machine will not have to adjust or change directory paths when reproducing results.


### Input data
Here are some suggested best practices for input data:

- Avoid renaming original data files.  Rather, if you need to rename them, create copies that then get renamed. This way there is always an original copy of the files as they were provided.
- In the `README.md` file, if appropriate, specify a contact person who provided the data and who can answer questions about the data.

### Using Git
Each research team should develop their own expectations for how often and when each researcher should commit changes to the git repository for the CLN. They should also define a strategy for git branching and perhaps quality control steps such as reviews at pull requests.  

#### What to Commit?
While git provide many benefits for project sharing, history, and concurrent work, it has limitations.  The most significant limitation is that large files should not be committed as they will slow down cloning and most online git services have limits on the size of repositories and files that can be committed.  The following are recommendations for what to commit:

- All `README.md` Files
- All `Methods.md` files, all R, Python or other scripts
- All the contents of the `00-docs` folder.
- Result files that are relatively small (e.g. images, data files, etc.)

What not to commit:

- Files larger than a few megabytes.
- Large files in the `01-input_data` folder

What to avoid committing:

- Intermediate files that are created in the process of performing analysis. These can be recreated if the `README.md`, `Methods.md` and notebooks are present and hence do not need to be backed up.
- Moderately sized result files.  These too can be recreated.


### Backups
The CLN standard described here is designed such that if followed all results can be reproduced by anyone provided that all necessary input data are available.  However, as described in the section "What to Commit?", the files in the `01-input_data` folder cannot be recreated and cannot be committed to the git repository if they are too big.  

However, it is critical that these input data are not lost in the event of catastrophic failure of the machine on which analysis is performed and where they are stored.  Therefore, at a minimum, all contents of the `01-input_data` folder should be backed up to ensure for disaster recovery.


### Limitations
This CLN strategy has several limitations. First, the reproducibility of any CLN is as good as the effort employed by the researchers to follow the standard and to provide proper notes, comments and instructions in the `README.md` files, the `Methods.md` files, scripts and notebooks.

Second, large files cannot be housed in git with the other files in the repository. This will require some coordination by anyone who clones the repository to retrieve the input data and rerun any tasks to reproduced larger result files.
