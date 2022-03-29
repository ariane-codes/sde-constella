# Constella Review Management Tool

Hello team! This is our repository, where we'll develop the product for Constella. Please read carefully before contributing.

## Install Dependencies

The first time you run this, you'll need to install the dependencies specified in `requirements.txt`. In order to do this, in your terminal, run:

```
pip install -r requirements.txt
```

You'll only need to do this once when you begin working on the project, and then every time a teammate adds a dependency.

## Environment Variables

In order to keep the database details secure, you've been given an `.env` file via Discord that you need to add to your local repo. This is ignored by Git and will not be uploaded, so as to keep the credentials safe. Make sure yo uplace the `.env` file at the root of your repository.

## Git Branching

I have disabled pushing and merging to `main` without a Pull Request with at least one approval. This means you must: 1. create a branch where you push your code, and 2. create a pull request in Github to request your code be merged to the `main` branch.

When you create your PR, make sure your branch is up to date and with no conflicts with `main`. You can do so by rebasing.

### About Branching
Give your branches a clear and helpful name. Not only for you, but for the rest of the team to navigate the repo more easily. For example, `db-fetch-users` if you're working on a function that connects to the database to fetch users.

### About Rebasing

When you're working on your branch, and someone merges a PR to `main`, your local branch is "behind", our outdated. If you want to push your changes and create a PR yourself, you'll first need to make sure your local branch is up-to-date.

Here's how I do it.

1. Start from your local branch. Add and commit your changes to prepare for the rest of the steps.
2. `git checkout main` to switch to the `main` branch.
3. `git pull origin main` to pull the changes from `main` in the remote repository.
4. `git checkout your-branch-name` to switch to your branch again.
5. `git rebase main` to rebase your branch from main. This command will:
   * rewind your commits
   * apply the commits you were missing from `main`
   * reapply your commits

Technically, you only need to do this if someone else merged to `main` while you were working on your branch. However, it's a good practice to **always** do this, just in case. Besides, it's good practice.

A tip: Do `git status` at any point if you're not sure where you left off or in which branch you are.

[Here's a cool video about rebasing, if you'd like to learn more.](https://www.youtube.com/watch?v=f1wnYdLEpgI&ab_channel=TheModernCoder)

### About Making a Pull Request (PR)

Make sure you have rebased from `main` and that your branch has no conflicts.

Also, please make your PR description as clear as possible. You've already made an effort to comment your code, and people will be reviewing your work, so add a general description that will help understand what your code does. Feel free to justify your choices and add screenshots, too.

### About Github Issues
We will use Issues when there are bugs in our development process. I will brief you about this when the time comes (when a bug arises, haha).

## Github and Trello

As you're working on your card, please attach the corresponding Github features to your cards. We will be attaching **branches, pull requests and issues.**

### Attach a branch

When you start working on a card, do the following:

1. `git checkout main` (in case you're not in `main`).
2. `git checkout -b your-descriptive-branch-name` to create your branch.
3. `git push origin your-descriptive-branch-name` to push your branch.

This will push your branch before you even start working on it, but it's okay, because it will let you connect it to your Trello card, and it will prevent your teammates from creating a branch with the same name.

Now, you can go to your Trello card and attach the branch. Simply click on the GitHub PowerUp and attach the branch, the name should appear on the list.

### Attach a Pull Request

Once you've finished your work on a Trello card, create a pull request on GitHub and also attach it to the card, in the same way you attached the branch. This will help us keep track of everyone's progress.
