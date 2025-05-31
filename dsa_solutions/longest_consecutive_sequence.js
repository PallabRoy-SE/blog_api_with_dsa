// Input: [100, 4, 200, 1, 3, 2];
// Output: 4;

function longestConsecutive(nums) {
  if (!nums?.length) return 0;

  const sequenceSet = new Set(nums);
  let maxSequence = 0;

  nums.forEach((number) => {
    if (!sequenceSet.has(number - 1)) {
      currMaxSequence = 1;
      currNumber = number;
      while (sequenceSet.has(currNumber + 1)) {
        currNumber++;
        currMaxSequence++;
      }
      maxSequence = Math.max(maxSequence, currMaxSequence);
    }
  });

  return maxSequence;
}

const input = [100, 4, 200, 1, 3, 2];
const output = longestConsecutive(input);
console.log(output);

const input2 = [100, 34, 200, 14, 36, 22];
const output2 = longestConsecutive(input2);
console.log(output2);
