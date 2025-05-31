// Input: [2, 2, 1, 1, 1, 2, 2];
// Output: 2;

function majorityElement(nums) {
  let element = -1;
  let vote = 0;

  nums.forEach((elem) => {
    if (vote === 0) {
      element = elem;
      vote++;
    } else {
      if (elem != element) vote--;
      else vote++;
    }
  });

  return element;
}

const input = [2, 2, 1, 1, 1, 2, 2];
const output = majorityElement(input);
console.log(output);

const input2 = [2, 2, 1, 1, 1];
const output2 = majorityElement(input2);
console.log(output2);
