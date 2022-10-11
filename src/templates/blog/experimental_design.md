<!-- META START
date_created: "2022-10-11"
META END -->
# How NOT to Design Experiments

Experiments with data is the essence of Data Science. You may find interesting patterns in data, predict something unknown from some known data, test a hypothesis based on data, etc. If you have good data, you can find wonders! However, if your experiment is not carefully designed, these wonders can be very misleading. Let's go through some common *experimental design* mistakes.

### Peeking
Consider the following situation: your lab needs to know whether a new drug A cures a certain disease quicker than the existing drug B. You decide to run A/B testing with a significance level of 5% (i.e., p-value < 0.05 would convince you that the new drug is indeed better). Initially you planned to make a trial with 200 patients in total. However, after you tested the new drug on the first 80 patients, you got p-value = 0.04. Yay! You report a success and stop the experiment to save the lab's money.

...Which you shouldn't have done. If you stop your experiment early whenever you breach the 0.05 threshold you'll get overly optimistic results. What you should've done is to continue your experiment until you've tested all 200 patients.

[My notebook demonstrates numerically](https://github.com/mysterious-ben/ds-examples/blob/master/mldesign/ab_testing_with_peeking.ipynb) how false positive rate surges 
- from 6% to 43% when the drugs are equally effective; and
- from 0% to 13% when the new drug is less effective.
More than a 40% chance to invest in a useless drug! If you want to save the lab's money, make your testing properly.

Note 1. This works the other way around too: if you stop your experiment early when the results do not look bright, you'll get pessimistic results instead.

Note 2. It works the same with confidence intervals.

Note 3. Do not confuse it with "early stopping" used to reduce overfitting of a Machine Learning model, which is a perfectly legitimate technique.

### Testing multiple hypotheses
In our busy times, beating a disease quicker is great but there are other things to consider as well. For example, the lab might want to check whether the new drug is safer. Or has fewer annoying short-term side effects. Or lower tolerance. Or whether it's more effective against a particular strain... Et cetera. Okay, can we check all these hypotheses at once? If the new drag beats the old drug in at least one domain, we may consider it to be a success and start producing it.

Yes... and no. If you test multiple hypotheses at once and decide that at least one success (in our case, p-value < 0.05) is an overall success, you reduce statistical significance of the test. For example, if you tested 5 hypotheses with significance level of 5% each, the combined significance level will be 1 - (0.95)^5 = 23%. For 10 hypotheses it will be 40%. So you'll have a 40% chance to invest in a new drug that is not actually better than the existing one. Yikes! 

[This article by Leihua Ye](https://towardsdatascience.com/multiple-comparison-a-common-pitfall-for-a-b-testing-d773f19a4a95) discusses a few methods to deal with this situation gracefully.

### Adding extra tests
Say, you designed your experiment properly and avoided the pitfalls described above. So your results are legit... but maybe they are not entirely satisfactory. If your p-value is 0.057 (while you expected it to be <0.05), you might decide to run tests on more samples to reduce the variance. If your model's accuracy is 51.4% (while you really need at least 52%), you might tweak your model a bit to reach that magical 52%. And hey, it's entirely possible that eventually you succeed!

Yeah... I know it. You know it =) You shouldn't have done that! If you modify your experiment whenever the outcome does not satisfy you, you get overly optimistic results. In fact, this is the overarching theme of [my previous article about overfitting](https://datascienceforhire.net/blog/art_of_overfitting).

Note. Unfortunately, in industry you can't always commit never to change your experiment. The requirements change, new ideas flow in, your budget may get cut, your boss may throw in his very important opinion. Just be aware: more ad hoc tweaks you make, less reliable your results will be.

### No baseline and success criteria
How good is good enough? When you don't know
- you'll likely have difficulties with defining your hypothesis clearly;
- you'll have trouble estimating whether you have enough data for your experiment (see below); and 
- you'll likely spend more time on research and will be tempted to add new tests because you don't know when to stop.

Note 1. In industry, you'll sometime get a research task without definite criteria of success. It's then up to you to make (at least) a rough estimate of what may count as success, based on your industry knowledge.

Note 2. Having a baseline also helps to produce meaningful success criteria. A baseline can be human performance, results of a previous study or a simple model, either ML or rule-based.

### Not enough data
This is an obvious one but it's often overlooked. Before you decide to test a hypothesis or validate a model, get at least a rough estimate of how much data you need to do it with some degree of certainty. For example, if you have just 20 data points, you're unlikely to spot a few-percent increase in efficiency of a new drug, or validate that this fancy deep neural network actually outperforms simple linear regression.

Here is a very convenient [sample size calculator](https://www.optimizely.com/sample-size-calculator/?conversion=10&effect=7&significance=95) that computes the minimum sample size for A/B testing.

### Ignoring biases in data
Depending on how your data was collected, it may or may not contain some nasty biases. This is especially true for manually collected data (e.g., via surveys). This topic really needs a separate article, so let's get back to it another day.

### Wrapping things up
The ideal experiment ~~that will never happen in the real world~~ will have all these steps:
1. Define your baseline and success criteria.
2. Define the hypothesis you're testing.
3. Write down the tests you'd like to perform to verify this hypothesis.
4. Account for biases in your data.
5. Ensure that you have enough data to get statistical significance.
6. Perform all the tests without stopping early or adding extra tests.
7. Brace yourself and check the results impartially (ideally, without seeing labels of your test cases).
8. Be strong to live with these results until the end of your life.

That's it for today! May the Good Experimental Design be with you.