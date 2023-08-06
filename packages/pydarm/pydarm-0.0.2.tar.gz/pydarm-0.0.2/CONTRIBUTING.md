# Contributing to pyDARM

## Overview

The `pyDARM` repository contiains the following directory structure:
* `docs`: documentation for pyDARM
* `examples`: examples for the use of pyDARM
* `model_files`: model file examples
* `pydarm`: source code for modeling the DARM control loop
* `test`: unit test resources for continuous integration

As a guideline, all `pyDARM` functions should include source code documentation at their header and a unit test in the appropriate file in the `test` directory.

## Unit tests

`pyDARM` includes a test suite, written using the
[unittest](https://docs.python.org/3/library/unittest.html) framework,
that attempts to test most of the functionality.  The tests can be run
from within the top level of the source with the following `unittest`
command:
```shell
$ python -m unittest discover
```
It can also be run with
[pytest](https://docs.pytest.org/en/stable/index.html):
```shell
$ pytest
```
(`pyDARM` is written in python3, so depending on your python install
the commands may be `python3 -m unittest` or `pytest-3`.)


## Brief summary - working with git

The general workflow should be as follows:
* [**Fork**](https://git.ligo.org/Calibration/pydarm/-/forks/new) the main repository:
  * always develop on a [fork](//doc.gitlab.com/ee/workflow/forking_workflow.html#creating-a-fork) of the upstream repository
* **Alternatively**, update an existing fork:
  * make sure your fork is linked to the upstream repo: `git remote add upstream git@git.ligo.org:Calibration/pydarm.git`
  * then sync the master branch from the upstream repo to your fork: `git pull --rebase upstream master`
* Create a new branch on your fork:
  * it is recommended that **all users** [develop on a branch](//doc.gitlab.com/ee/workflow/forking_workflow.html#creating-a-fork) made specifically for this change - this leaves the `master` branch of your fork as a landing place for upstream changes from other developments
* Make some commits and `git push` them to your fork on git.ligo.org
* Open a merge request:
  * go to your fork on git.ligo.org and there should be a button - this will allow the changes to be reviewed before acceptance, modification request, or rejection, and you can iterate with the repository owners, often in real-time
  * any subsequent commits you push to your development branch will automatically be added to the request
* Delete your development branch:
  * if the request is merged, git.ligo.org will allow you to delete your development branch, keeping your fork clean for future work

For more information, here's a [quick reference](//gitref.org/basic/) for the basic git commands (`init`, `clone`, `status`, `add`, `commit`, `push`, `pull`).

## Detailed contribution guide

If you wish to contribute new code, or changes to existing code, please follow this development workflow:

### Make a fork (copy) of pyDARM

**You only need to do this once**

1. Go to the [pyDARM repository home page](https://git.ligo.org/Calibration/pydarm)
2. Click on the *Fork* button, that should lead you [here](https://git.ligo.org/Calibration/pydarm/-/forks/new)
3. Select the namespace that you want to create the fork in, this will usually be your personal namespace

If you can't see the *Fork* button, make sure that you are logged in by checking for your account profile photo in the top right-hand corner of the screen.

### Clone your fork

Make sure that you have installed and configured [git-lfs](https://wiki.ligo.org/Computing/GitLFS#Install_the_git_LFS_client) for the management of large files. This is required to successfully build and install your development fork. 

Then, clone your fork with 

```bash
git clone git@git.ligo.org:<namespace>/pydarm.git
```

### Keeping your fork up to date

Link your clone to the main (`upstream`) repository so that you can `fetch` changes, `merge` them with your clone, and `push` them to your fork. Do *not* make changes on your master branch. 

1. Link your fork to the main repository:

    ```bash
    cd pydarm
    git remote add upstream git@git.ligo.org:Calibration/pydarm.git
    ```

    You need only do this step once.

2. Fetch new changes from the `upstream` repository, merge them with your master branch, and push them to your fork on git.ligo.org:

    ```bash
    git checkout master
    git fetch upstream
    git merge upstream/master
    git push
    ```

3. You can see which remotes are configured using

   ```bash
   git remote -v
   ```

   If you have followed the instructions thus far, you should see four lines. Lines one and two begin with `origin` and reference your fork on git.ligo.org with both `fetch` and `push` methods. Lines three and four begin with `upstream` and refer to the main repository on git.ligo.org with both `fetch` and `push` methods.

### Making changes

All changes should be developed on a feature branch in order to keep them separate from other work, thus simplifying the review and merge once the work is complete. The workflow is:

1. Create a new feature branch configured to track the `master` branch of the `upstream` repository:

   ```bash
   git checkout -b my-new-feature upstream/master
   ```

   This command creates the new branch `my-new-feature`, sets up tracking the `upstream` repository, and checks out the new branch. It also automatically switches you to that branch. There are other ways to do these steps, but this is a good habit since it will allow you to `fetch` and `merge` changes from `upstream/master` directly onto the branch.

2. Develop the changes you would like to introduce, using `git commit` to finalise a specific change.
   Ideally commit small units of change often, rather than creating one large commit at the end, this will simplify review and make modifying any changes easier.

   Commit messages should be clear, identifying which code was changed, and why.
   Common practice is to use a short summary line (<50 characters), followed by a blank line, then more information in longer lines.

3. Push your changes to the remote copy of your fork on https://git.ligo.org.
   The first `push` of any new feature branch will require the `-u/--set-upstream` option to `push` to create a link between your new branch and the `origin` remote:

    ```bash
    git push --set-upstream origin my-new-feature
    ```

    Subsequent pushes can be made with 

    ```bash
    git push origin my-new-feature
    ```

4. Keep your feature branch up to date with the `upstream` repository by doing 

   ```bash
   git checkout my-new-feature
   git fetch upstream
   git rebase upstream/master
   git push -f origin my-new-feature
   ```

   This works if you created your branch with the `checkout` command above. If you forgot to add the `upstream/master` starting point, then you will need to dig deeper into git commands to get changes and merge them into your feature branch. 

   If there are conflicts between `upstream` changes and your changes, you will need to resolve them before pushing everything to your fork. 

### Open a merge request

When you feel that your work is finished, you should create a merge request to propose that your changes be merged into the main (`upstream`) repository.

After you have pushed your new feature branch to `origin`, you should find a new button on the [pyDARM repository home page](https://git.ligo.org/Calibration/pydarm/) inviting you to create a merge request out of your newly pushed branch. (If the button does not exist, you can initiate a merge request by going to the `Merge Requests` tab on your fork website on git.ligo.org and clicking `New merge request`)

You should click the button, and proceed to fill in the title and description boxes on the merge request page. It is recommended that you check the box to `Delete source branch when merge request is accepted` (it is checked by default); this will result in the branch being automatically removed from your remote fork when the merge request is accepted.

Once the request has been opened, one of the maintainers will assign someone to review the change. There may be suggestions and/or discussion with the reviewer. These interactions are intended to make the resulting changes better. Once satisfied, the reviewer can approve and merge your request.

### Post-merge request - cleanup

Once the changes are merged into the upstream repository the remote feature branch is deleted from your fork (because `Delete source branch when merge request is accepted` was checked in the merge request). The feature branch remains on your local clone, so you should remove this from your local clone by first pulling in the latest vers ion of the `upstream/master` and then deleting the branch. This can be done using 

   ```bash
    git checkout master
    git fetch upstream
    git merge upstream/master
    git push
    git branch -d my-new-feature
   ```

A feature branch should *not* be repurposed for further development as this can result in problems merging upstream changes.

## Other use cases
The above workflow should be the one all development should follow. Other workflows may require more detailed understanding of git. Help for resolving issues in those situations is not guaranteed.

### Assist with a feature branch
If one wants to contribute to a feature branch of another user, `<albert.einstein>`, then one adds the other user's repository as a remote, making a new local branch from their feature branch.

After adding the other user's repository as a remote, a list of available branches can be found via `git branch --remote`. Alternatively, the web interface to the git repository can be browsed to find different available branches (Repository > Branches on the sidebar menu of that user's fork of the repository).

   ```bash
   git remote add <name> git@git.ligo.org:<albert-einstein>/pydarm.git
   git fetch <name>
   git checkout new-feature
   <make changes>
   <commit changes>
   git push <name> new-feature
   ```

Here, `<name>` can be anything descriptive like `dev-help`, `new-feature` should be what the other user's feature branch is called, and replace `<albert-einstein>` with the other user's LIGO.ORG username (note the hyphen here and not a dot; in most cases, users on git.ligo.org have a hyphen in their username, but a few users have a dot--take note of the situation you are working in).

This should allow you to make changes on the feature branch, commit those changes, and push to the remote branch. *The branch owner and anyone assisting will need to coordinate development and pushing/pulling to the remote branch.* If a merge request had been opened to merge that branch to `upstream/master`, then the new changes should also appear in the merge request. Once you are done assisting, then you can switch back to your main branch and remove the remote.

   ```bash
    git checkout master
    git remote remove <name>
    git branch -d new-feature
   ```

Depending on the status of the branch (e.g., git may complain that it has not been merged), you may need to use the `-D` option to force deletion of your local copy of the branch if that is what you really want to do. Note that using `-d` or `-D` does not delete the remote branch so you can always check it out again if desired.

### Fork-and-merge on another user's feature branch
Alternatively, if there is active development by the owner of the feature branch on it and one wants to contribute, then it is most straightforward to simply create a fork of the repo that has already been forked. Then, follow the [instructions for normally contributing via the fork-and-merge workflow](#detailed-contribution-guide), but instead of the `upstream` pointing to `Calibration/pydarm.git`, instead you point the `upstream` to `<albert-einstein>/pydarm.git`. One would then fetch the branch, make a branch from that branch, and when making the merge request, point the merge request to the specified target (the original feature branch).

Assuming one has already forked off of the fork containing the feature branch, we can make the following steps to begin contributing to the feature branch on another fork. **Note: Gitlab cannot have two projects named the same in a single namespace even if they are forked from two different repositories. You need to give the new fork a different name/project slug besides `pydarm` because you may already have forked the main `pydarm` project and it is already called `pydarm` in your local namespace.**

   ```bash
   git clone git@git.ligo.org:<albert-einstein>/<pydarm-users-repo>.git
   cd <pydarm-users-repo>
   git remote add upstream git@git.ligo.org:<other-users-albert-einstein>/pydarm.git
   git checkout master
   git fetch upstream
   git merge upstream/master
   git push
   git checkout <feature-branch>
   git checkout -b <new-feature> upstream/<feature-branch>
   ...make changes...
   ...commit changes...
   git push --set-upstream origin <new-feature>
   ```

One would then need to create the merge request onto the target feature branch (`<feature-branch>`) of the fork using the web interface or the link provided on the terminal, paying attention to the source branch (`<new-feature>`) and target branches.

### Keep separate production and development copies of `pyDARM`
**Note: this is not a suggested workflow because it is easy to confuse which code one should develop. Mistakes are easy to make following this workflow and it is discouraged.**

In the future, this should be completely unneeded because production `pyDARM` will be available via PyPI and conda-forge. For now, however, if one wants to have a production version available for running the current, vetted version of `pyDARM`, and, separately, a development version, then this can be done by the following. One can install a snapshot of the `pyDARM:master` into a location specified by `--prefix` and use the `PYTHONPATH` environment variable to switch between the two installations at runtime.

   ```bash
   python3 setup.py install --prefix=../pydarm
   export PYTHONPATH=<full-path-to-../pydarm>
   ```
where you would replace `<full-path-to-../pydarm>` with the full path from the `--prefix` path.

Alternatively one could keep two git clones, for example keeping both the production and development clones will be in the same base directory. We will call the development clone `pydarm-devel` which needs to be a fork of the repository (see above for how to do this). One could also put the two repository clones in different base directories so that both clones can reside in `pydarm` directories. It is best practice not to keep separate copies in any case, but doing so it is up to the user to manage their own clones of the repository.

   ```bash
   git clone git@git.ligo.org:Calibration/pydarm.git
   git clone git@git.ligo.org:<albert.einstein>/pydarm.git pydarm-devel
   cd pydarm-devel
   ```

One can then use the `pydarm-devel` checkout as described above in the usual workflow for development.

**We repeat again that this workflow is discouraged and simply following the typical workflow should work in all circumstances will work for users over the long term.**

## git tips and tricks
If you are unfamiliar with git, [atlassian has an excellent series of tutorials](https://www.atlassian.com/git/tutorials). If you are new to git, it is highly recommended to go through some of these tutorials to gain some familliarity with basic commands.

Using the `git stash` is extremely useful when you are working on something in a branch, realize you want to change to a different branch but hang on to your changes without commiting. The workflow might be something along the lines of

   ```bash
   <edit and some files in branch FOO>
   git stash
   git checkout <some other branch>
   <do some other work>
   <either commit or stash the other work>
   git checkout <FOO>
   git stash list
   git stash pop stash@{<number>}
   ```

Jeff has a few quick tips to get familiar as well.

Once you're at the "multiple branches under development" stage of your life, here're some useful commands
   ```bash
    git checkout -b <branchname> upstream/master ->  creates new branch tracking the upstream master branch
    git branch                                   ->  lists all branches
    git checkout <branchname>                    ->  switches to <branchname>
   ```
Then implement your changes on your branch using `git add <filename>` and `git commit <filename>` or `git commit -a` to finalise a specific changes to files, or to repo structure. After, push to your namespace using `git push --set-upstream origin <branchname>` This explanation is detailed better in the above contribution guide.
