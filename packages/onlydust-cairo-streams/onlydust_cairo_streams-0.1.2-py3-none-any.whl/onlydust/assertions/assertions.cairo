%lang starknet

func assert_felt(a : felt, assertion : codeoffset, b : felt):
    [ap] = a; ap++
    [ap] = b; ap++
    call abs assertion
    ret
end

func is_equal_to(a : felt, b : felt):
    assert a = b
    ret
end

func test():
    let a = 42
    let b = 42
    assert_that(a, is_equal_to, b)
end
