// You can edit this code!
// Click here and start typing.
package main

import (
	"container/heap"
	_ "embed"
	"fmt"
	"regexp"
	"sort"
	"strings"
)

var re = regexp.MustCompile(`The (\w+) floor contains`)
var split = regexp.MustCompile(`(and|,)`)

var levelsByFloor = map[string]int{
	"first":  1,
	"second": 2,
	"third":  3,
	"fourth": 4,
}

//go:embed example.txt
var example string

func main() {
	fmt.Println("part 1:", bfs(parse(input)))

	floors := parse(input)
	newFloor := NewSet()
	newFloor.Add(floors[1].List()...)
	newFloor.Add("elerium", "dilithium", "elerium generator", "dilithium generator")
	floors[1] = *newFloor
	fmt.Println("part 2:", bfs(floors))
}

func parse(input string) map[int]Set {
	input = strings.TrimSpace(input)
	floors := make(map[int]Set)
	for i := 1; i <= 4; i++ {
		floors[i] = *NewSet()
	}
	input = strings.ReplaceAll(input, " a ", " ")
	input = strings.ReplaceAll(input, ".", "")
	input = strings.ReplaceAll(input, "-", " ")
	lines := strings.Split(input, "\n")
	for _, line := range lines {
		if strings.Contains(line, "nothing") {
			continue
		}
		m := re.FindAllStringSubmatch(line, -1)
		level := levelsByFloor[m[0][1]]
		line = re.ReplaceAllString(line, "")
		items := split.Split(line, -1)
		set := NewSet()
		for _, item := range items {
			item = strings.TrimSpace(item)
			if item == "" {
				continue
			}
			set.Add(item)
		}
		floors[level] = *set
	}
	return floors
}

func bfs(floors map[int]Set) int {
	pq := make(PriorityQueue, 1, 1e6)
	pq[0] = &Item{
		steps:  0,
		level:  1,
		floors: floors,
	}
	n := 0
	for _, floor := range floors {
		n += floor.Len()
	}
	cache := make(map[string]bool)
	fried := make(map[string]bool)

	isFried := func(items []string) bool {
		sort.Strings(items)
		key := fmt.Sprint(items)
		if v, ok := fried[key]; ok {
			return v
		}
		fried[key] = isChipFried(items)
		return fried[key]
	}

	iter := 0
	for pq.Len() > 0 {
		iter++
		item := heap.Pop(&pq).(*Item)
		if item.level == 4 && item.floors[4].Len() == n {
			return item.steps
		}

		if iter%1e5 == 0 {
			fmt.Println("iter:", iter, "steps:", item.steps)
		}

		if _, ok := cache[item.String()]; ok {
			continue
		}
		cache[item.String()] = true

		items := item.floors[item.level].List()
		if isFried(items) {
			continue
		}

		var combinations [][]string
		for i, lhs := range items {
			for _, rhs := range items[i+1:] {
				combinations = append(combinations, []string{lhs, rhs})
			}
			combinations = append(combinations, []string{lhs})
		}

		for _, items := range combinations {
			if isFried(items) {
				continue
			}
			// Move down with 1 item.
			if item.level > 1 && len(items) == 1 {
				newFloors := make(map[int]Set)
				for k, v := range item.floors {
					newFloors[k] = v
				}
				if lower, ok := newFloors[item.level-1]; ok {
					newLower := NewSet(lower.List()...)
					newLower.Add(items...)
					newFloors[item.level-1] = *newLower

					curr := newFloors[item.level]
					newCurr := NewSet(curr.List()...)
					newCurr.Remove(items...)
					newFloors[item.level] = *newCurr

					newItem := &Item{
						steps:  item.steps + 1,
						level:  item.level - 1,
						floors: newFloors,
						index:  item.index + 1,
					}

					if !isFried(newLower.List()) && !isFried(newCurr.List()) && !cache[newItem.String()] {
						heap.Push(&pq, newItem)
					}
				}
			}
			// Move up with 2 items.
			if item.level < 4 && len(items) == 2 {
				newFloors := make(map[int]Set)
				for k, v := range item.floors {
					newFloors[k] = v
				}
				if upper, ok := newFloors[item.level+1]; ok {
					newUpper := NewSet(upper.List()...)
					newUpper.Add(items...)
					newFloors[item.level+1] = *newUpper

					curr := newFloors[item.level]
					newCurr := NewSet(curr.List()...)
					newCurr.Remove(items...)
					newFloors[item.level] = *newCurr

					newItem := &Item{
						steps:  item.steps + 1,
						level:  item.level + 1,
						floors: newFloors,
						index:  item.index + 1,
					}
					if !isFried(newUpper.List()) && !isFried(newCurr.List()) && !cache[newItem.String()] {
						heap.Push(&pq, newItem)
					}
				}
			}
		}
	}

	return 0
}

func isChipFried(items []string) bool {
	generators, microchips := NewSet(), NewSet()
	for _, item := range items {
		parts := strings.Fields(item)
		name := parts[0]
		if strings.HasSuffix(item, "generator") {
			generators.Add(name)
		} else {
			microchips.Add(name)
		}
	}

	return generators.Len() > 0 && microchips.Difference(generators).Len() > 0
}

type Item struct {
	floors map[int]Set
	steps  int
	level  int
	index  int
}

func (it Item) String() string {
	var key []string
	for i := 1; i <= 4; i++ {
		items := it.floors[i].List()
		sort.Strings(items)
		key = append(key, fmt.Sprintf("%d: %v", i, items))
	}

	key = append(key, fmt.Sprintf("level: %d", it.level))
	return strings.Join(key, " ")
}

// A PriorityQueue implements heap.Interface and holds Items.
type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	lhs, rhs := pq[i], pq[j]
	byIndex := lhs.index - rhs.index
	byLevel := lhs.floors[4].Len() - rhs.floors[4].Len() // Focus on the 4th floor.
	bySteps := lhs.steps - rhs.steps
	_ = bySteps
	_ = byIndex // Uncomment this for BFS.
	// -tive byIndex means DFS.
	return sortBy(-byIndex, -byLevel)
}

func sortBy(sc ...int) bool {
	for _, s := range sc {
		if s != 0 {
			return s < 0
		}
	}
	return false
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
}

func (pq *PriorityQueue) Push(x interface{}) {
	item := x.(*Item)
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil // avoid memory leak
	*pq = old[0 : n-1]
	return item
}

type Set struct {
	value map[string]bool
}

func NewSet(items ...string) *Set {
	s := &Set{
		value: make(map[string]bool),
	}
	s.Add(items...)
	return s
}

func (s Set) Len() int {
	return len(s.value)
}

func (s *Set) Add(items ...string) {
	for _, item := range items {
		s.value[item] = true
	}
}

func (s *Set) Remove(items ...string) {
	for _, item := range items {
		delete(s.value, item)
	}
}

func (s Set) Map() map[string]bool {
	m := make(map[string]bool)
	for k, v := range s.value {
		m[k] = v
	}
	return m
}

func (s Set) List() []string {
	var result []string
	for k := range s.value {
		result = append(result, k)
	}
	return result
}

func (s Set) Difference(other *Set) *Set {
	m := NewSet(s.List()...)
	m.Remove(other.List()...)
	return m
}

var input = `The first floor contains a polonium generator, a thulium generator, a thulium-compatible microchip, a promethium generator, a ruthenium generator, a ruthenium-compatible microchip, a cobalt generator, and a cobalt-compatible microchip.
The second floor contains a polonium-compatible microchip and a promethium-compatible microchip.
The third floor contains nothing relevant.
The fourth floor contains nothing relevant.`
