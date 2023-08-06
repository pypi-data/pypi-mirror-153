;; this file is the ChiakiLisp core library, feel free to update it!
(import functools)
(import chiakilisp.lexer)
(import chiakilisp.parser)
(import chiakilisp.runtime)
;; be able to reference already imported 'functools/reduce' function
(def reduce functools/reduce)
;; set of general purpose functions like (identity ...) or something
(defn identity (x)
 x)
;; very simple functions for common number types operations covering
(defn inc (x)
 ;; returns number incremented by 1
 (+ x 1))
(defn dec (x)
 ;; returns number decremented by 1
 (- x 1))
(defn odd? (x)
 ;; returns true if the number is not even
 (not (even? x)))
(defn zero? (x)
 ;; returns true if the number equals to 0
 (= x 0))
(defn positive? (x)
 ;; returns true if the number is bigger than 0
 (> x 0))
(defn even? (x)
 ;; returns true if the number is even (X % 2 == 0)
 (= (mod x 2) 0))
;; very simple functions for the type-checking procedure simplifying
(defn nil? (x)
 ;; returns true if X is nil (or NoneType, if you are more Pythonic)
 (= x nil))
(defn int? (x)
 ;; returns true if X is an instance of `int` (an integer value)
 (isinstance x int))
(defn set? (x)
 ;; returns true if X is an instance of `set` (a set data structure)
 (isinstance x set))
(defn str? (x)
 ;; returns true if X is an instance of `str` (a string value)
 (isinstance x str))
(defn list? (x)
 ;; returns true if X is an instance of `list` (list data structure)
 (isinstance x list))
(defn dict? (x)
 ;; returns true if X is an instance of `dict` (dict data structure)
 (isinstance x dict))
(defn bool? (x)
 ;; returns true if X is an instance of `bool` (a boolean value)
 (isinstance x bool))
(defn float? (x)
 ;; returns true if X is an instance of `float` (float-number value)
 (isinstance x float))
(defn tuple? (x)
 ;; returns true if X is an instance of `tuple` (tuple' data struct)
 (isinstance x tuple))
(defn = (first second)
 ;; returns true if first equals to second
 (.__eq__ first second))
(defn < (first second)
 ;; returns true if first less than second
 (.__lt__ first second))
(defn > (first second)
 ;; returns true if first greater than second
 (.__gt__ first second))
(defn <= (first second)
 ;; returns true if first less-than-equals-to second
 (.__le__ first second))
(defn >= (first second)
 ;; returns true if first is greater-than-equals-to second
 (.__ge__ first second))
;; 'clojure-world' functions to operate the Python 3 data structures
(defn count (x)
 ;; returns number of collection elements (list, tuple, dict or str)
 (.__len__ x))
(defn contains? (coll item)
 ;; returns true if collection contains item
 (when (set? coll)
  (.__contains__ coll item)))
(defn not (x)
 ;; returns false if X is "truthy", otherwise returns false
 (if x false true))
(defn get (& args)
 ;; allows to safely get an item from: list, tuple, dict or a string
 ;; hint for the future: could not use destructuring in get function
 (when (>= (count args) 2)
  (let (coll (.__getitem__ args 0)
        item (.__getitem__ args 1))
   (cond (= 2 (count args)) (get coll item nil)
         (= 3 (count args))
         (let (default (.__getitem__ args 2))
          (cond (set? coll) (when (contains? coll item) item)
                (and (or (str? coll)
                         (list? coll)
                         (tuple? coll))
                     (int? item)) (try (.__getitem__ coll item)
                                   (catch IndexError _ default))
                (dict? coll) (try (.__getitem__ coll item)
                                   (catch KeyError _ default))))))))
(defn first (coll)
 ;; returns first element of given list, tuple or str data structure
 (when (or (list? coll) (tuple? coll) (str? coll))
  (get coll 0)))
(defn last (coll)
 ;; returns last element of given list, tuple or str data structure
 (when (or (list? coll) (tuple? coll) (str? coll))
  (get coll (- 0 1))))
(defn second (coll)
 ;; returns second element of the list, tuple or str data structure
 (when (or (list? coll) (tuple? coll))
  (get coll 1)))
(defn third (coll)
 ;; returns third element of given list, tuple or str data structure
 (when (or (list? coll) (tuple? coll))
  (get coll 2)))
(defn rest (coll)
 ;; returns rest items (means everything but first) of list or tuple
 (when (and coll
            (or (list? coll)
                (tuple? coll)))
  (let (new (list coll)
        rev (-> new reversed list))
   (.pop rev)
   (-> rev reversed list))))
(defn get-in (& args)
 ;; allows to safely (get ...) a value from a collection by its path
 (when args
  (let ((coll path default) args)
        (cond (>= (count args) 2)
              (functools/reduce (fn (acc n)
                                  (get acc n default)) path coll)))))
(defn conj (& args)
 ;; basically, this function behaves like the clojure 'conj' function
 (when args
  (if (= 1 (count args))
   (first args)
   (let (coll (first args)
         items (rest args))
    (cond (set? coll)
          (let (new (list coll)) (.extend new items) (set new))
          (list? coll)
          (let (new (list coll)) (.extend new items) new)
          (tuple? coll)
          (let (new (list coll)) (.extend new items) (tuple new))
          (dict? coll)
          (let (new (dict coll)) (functools/reduce (fn (acc new)
                                                    (.update acc new)
                                                    acc)
                                  items new)))))))
(defn into (to from)
 ;; basically, this function behaves like the clojure `into` function
 (functools/reduce conj to from))
(defn juxt (& functions)
 ;; basically, this function behaves like the clojure `juxt` function
 (fn (x) (map (fn (f) (f x)) functions)))
(defn select-strs (coll strs)
 ;; allows to select concrete strs from the given dictionary instance
 (when (and (dict? coll) (or (list? strs) (tuple? strs) (set? coll)))
  (filter (fn (kv-pair)
           (let ((k _) kv-pair) (contains? strs k))) (.items coll))))
(defn eval (source)
 ;; evaluates a ChiakiLisp program ... inside of a ChiakiLisp program
 (let (lexer  (lexer/Lexer source "<eval>")
       _      (.lex lexer)
       parser (parser/Parser (.tokens lexer))
       _      (.parse parser)
       wood   (.wood parser))
  (->> wood
       (map (fn (an-expr) (.execute an-expr runtime/ENVIRONMENT))))))