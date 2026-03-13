/* ======================================
   ソートアルゴリズム Step生成
====================================== */

const STEP = Object.freeze({
  COMPARE: "compare",
  SWAP: "swap",
  SET: "set",
  SPLIT: "split",
  FINALIZE: "finalize"
})

/* ==============================
   Bubble Sort
============================== */

function bubbleSteps(values){

  const a = values.slice()
  const steps = []

  const n = a.length

  for(let i=0;i<n;i++){

    steps.push({type:STEP.SPLIT,range:[0,n-i-1]})

    for(let j=0;j<n-i-1;j++){

      steps.push({type:STEP.COMPARE,i:j,j:j+1})

      if(a[j] > a[j+1]){

        [a[j],a[j+1]]=[a[j+1],a[j]]

        steps.push({type:STEP.SWAP,i:j,j:j+1})

      }

    }

    steps.push({type:STEP.FINALIZE,index:n-i-1})

  }

  return steps

}

/* ==============================
   Selection Sort
============================== */

function selectionSteps(values){

  const a = values.slice()
  const steps = []

  const n = a.length

  for(let i=0;i<n;i++){

    let min = i

    steps.push({type:STEP.SPLIT,range:[i,n-1]})

    for(let j=i+1;j<n;j++){

      steps.push({type:STEP.COMPARE,i:min,j:j})

      if(a[j] < a[min]) min = j

    }

    if(min !== i){

      [a[i],a[min]]=[a[min],a[i]]

      steps.push({type:STEP.SWAP,i:i,j:min})

    }

    steps.push({type:STEP.FINALIZE,index:i})

  }

  return steps

}

/* ==============================
   Insertion Sort
============================== */

function insertionSteps(values){

  const a = values.slice()
  const steps = []

  if(a.length>0)
    steps.push({type:STEP.FINALIZE,index:0})

  for(let i=1;i<a.length;i++){

    let j=i

    while(j>0){

      steps.push({type:STEP.COMPARE,i:j-1,j:j})

      if(a[j-1] <= a[j]) break

      [a[j-1],a[j]]=[a[j],a[j-1]]

      steps.push({type:STEP.SWAP,i:j-1,j:j})

      j--

    }

    steps.push({type:STEP.FINALIZE,index:i})

  }

  return steps

}

/* ==============================
   Merge Sort
============================== */

function mergeSteps(values){

  const arr = values.slice()
  const steps = []

  function sort(l,r){

    if(l>=r) return

    const m = Math.floor((l+r)/2)

    sort(l,m)
    sort(m+1,r)

    let i=l
    let j=m+1

    const temp=[]

    while(i<=m && j<=r){

      steps.push({type:STEP.COMPARE,i:i,j:j})

      if(arr[i] <= arr[j]) temp.push(arr[i++])
      else temp.push(arr[j++])

    }

    while(i<=m) temp.push(arr[i++])
    while(j<=r) temp.push(arr[j++])

    for(let k=0;k<temp.length;k++){

      arr[l+k]=temp[k]

      steps.push({
        type:STEP.SET,
        index:l+k,
        value:temp[k]
      })

    }

  }

  sort(0,arr.length-1)

  for(let i=0;i<arr.length;i++)
    steps.push({type:STEP.FINALIZE,index:i})

  return steps

}

/* ==============================
   Quick Sort
============================== */

function quickSteps(values){

  const a = values.slice()
  const steps = []

  function sort(l,r){

    if(l>=r) return

    const pivot = a[r]

    let i=l

    for(let j=l;j<r;j++){

      steps.push({type:STEP.COMPARE,i:j,j:r})

      if(a[j] < pivot){

        [a[i],a[j]]=[a[j],a[i]]

        steps.push({type:STEP.SWAP,i:i,j:j})

        i++

      }

    }

    [a[i],a[r]]=[a[r],a[i]]

    steps.push({type:STEP.SWAP,i:i,j:r})

    steps.push({type:STEP.FINALIZE,index:i})

    sort(l,i-1)
    sort(i+1,r)

  }

  sort(0,a.length-1)

  return steps

}

/* ==============================
   Heap Sort
============================== */

function heapSteps(values){

  const a = values.slice()
  const steps = []

  function heapify(n,i){

    let largest = i

    const l = 2*i + 1
    const r = 2*i + 2

    if(l<n){

      steps.push({type:STEP.COMPARE,i:largest,j:l})

      if(a[l] > a[largest]) largest = l

    }

    if(r<n){

      steps.push({type:STEP.COMPARE,i:largest,j:r})

      if(a[r] > a[largest]) largest = r

    }

    if(largest !== i){

      [a[i],a[largest]]=[a[largest],a[i]]

      steps.push({type:STEP.SWAP,i:i,j:largest})

      heapify(n,largest)

    }

  }

  const n = a.length

  /* heap構築 */

  for(let i=Math.floor(n/2)-1;i>=0;i--){

    heapify(n,i)

  }

  /* ソート */

  for(let i=n-1;i>0;i--){

    [a[0],a[i]]=[a[i],a[0]]

    steps.push({type:STEP.SWAP,i:0,j:i})

    steps.push({type:STEP.FINALIZE,index:i})

    heapify(i,0)

  }

  steps.push({type:STEP.FINALIZE,index:0})

  return steps

}