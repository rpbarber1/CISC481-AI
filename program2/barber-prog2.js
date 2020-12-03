/*
    Ryan Barber
    CISC 481
    Program 2 - N-Queens
*/


class Node{
    constructor(assigned, vars){
        this.assigned_list = assigned
        this.vars_doms = vars
        this.next_node = null
    }
}
//===============================================

/*
#This function will create the problem parameters
# n - number of queens/ size of board nxn
*/
function setup(n){
    /*
    Close to same set up as in writeup
    #CSP = [[variable_domains], [constriants]]
    # variable_domains = [[1,2,3,n], [1,2,3,n], n[]]
    # constraints = [var1_idx, var2_idx, pair1, pair2, pairN]
    #   pair = [var1-domain-idx, var2-domain-idx]
    */

    //vars_doms
    //variable number (index of vars_doms) = queen number
    //the array at that variable = domain
    var vars_doms = []
    for(i = 0; i < n; i++){
        var dom = []
        for(j = 0; j < n; j++){
            dom.push(j)
        }
        vars_doms.push(dom)
    }

    //constraints
    var constraints = []
    for(i = 0; i < n; i++){
        for(j = i+1; j < n; j++){
            //var1-idx = i
            //var2-idx = j
            var tmp_constraint = [i, j]
            var tmp_pair = []
            for(p = 0; p < n; p++){
                for(q = 0; q < n; q++){
                    if((p != q) && ((Math.abs(p-q)) / (Math.abs(i-j))) != 1){
                        tmp_pair = [p,q]
                        tmp_constraint.push(tmp_pair)
                    }
                }
            }
            constraints.push(tmp_constraint)
        }
    }
    return [vars_doms , constraints]
}
//===============================================

/*
    csp = [vars_doms, constrains]
    var1 = index of vars_doms = queen number
    var2 = index of vars_doms = queen number
*/
function revise(csp, var1, var2) {
    var revised = false

    //get constraint we want to check against
    var constraint_to_check = []
    var reversed = false
    //for each constraint
    for(i = 0; i<csp[1].length; i++){
        if((csp[1][i][0] == var1) && (csp[1][i][1] == var2)){
            constraint_to_check = csp[1][i]
        }
        else if(csp[1][i][0] == var2 && csp[1][i][1] == var1){
            constraint_to_check = csp[1][i]
            reversed = true
            
        }
    }
    //do revision
    for(i = 0; i < csp[0][var1].length; i++){
        remove_i = true
        for(j = 0; j < csp[0][var2].length; j++){
            if(remove_i == false){
                break
            }
            //tmp = [var1-value, var2-value]
            if(reversed){
                var tmp = [csp[0][var2][j],csp[0][var1][i]]
            }else {
                var tmp = [csp[0][var1][i], csp[0][var2][j]]
            }
            for(k = 2; k < constraint_to_check.length; k++){
                if((tmp[0] == constraint_to_check[k][0]) && (tmp[1] == constraint_to_check[k][1])){
                    remove_i = false
                    break
                }
            }
        }
        if(remove_i){//if removing; set that value to -1
            //console.log("removing value: ["+csp[0][var1][i]+"] from Queen-"+var1)
            delete csp[0][var1][i]
            revised = true
        }
    }
    var row = []
    csp[0][var1].forEach(function(element){
        if(element != undefined){
            row.push(element)
        }
    })
    csp[0][var1] = row
    return [revised,csp]
}
//===============================================
function ac3(csp){
    //set initail arcs
    var arcs = []
    for(i = 0; i < csp[0].length; i++){
        for(j = 0; j < csp[0].length; j++){
            if(i==j){
                continue
            }
            var arc = [i,j]
            arcs.push(arc)
        }
    }
    var updated_csp = JSON.parse(JSON.stringify(csp))
    //loop through arcs poping(shift()) and pushing 
    while(arcs.length != 0){
        //get and remove first element of arcs
        var arc = arcs.shift()
        var result = revise(updated_csp, arc[0], arc[1])
        var updated_csp = result[1]
        if(result[0]){
            //generate all arcs with second value (q) = current arc first value (arc[0])
            // we have to recheck because the domain has changed
            for(i = 0; i < updated_csp[1].length; i++){
                var tmp_arc = null
                //loop through all variable combinations
                //find a possible arc
                //check its not in arcs list
                //add to end
                for(p = 0; p < csp[0].length; p++){
                    for(q = 0; q < csp[0].length; q++){
                        if(p==q){
                            continue
                        }
                        if(arc[0] = q){
                            tmp_arc = [p,q] //found possible arc
                            //check if its in arcs already
                            var in_arcs = false
                            for(r = 0; r < arcs.length; r++){
                                if(arcs[r][0] == tmp_arc[0] && arcs[r][1] == tmp_arc[1]){
                                    in_arcs = true 
                                    break
                                }
                            }
                            if(in_arcs){
                                continue
                            }
                            arcs.push(tmp_arc)
                        }
                    }
                }
            }
        }
    }
    //check if all queens have at least 1 valid domain value
    one_valid = true
    for(i = 0; i < updated_csp[0].length; i++){
        if(updated_csp[0].length == 0){
            one_valid = false
            break
        }
    }
    //if there's no valid value: return false
    if(!one_valid){
        return false
    }
    //there is a valid value for all queens
    return [true,updated_csp]
}
//===============================================
/*
    assigned_list = [queen-a, queen-b,...]
        queen-a = value = index in csp[0]
*/
function minimumRemainingValues(csp, assigned_list){
    var best = null
    var best_count = 0

    for(i = 0; i < csp[0].length; i++){
        var already_assigned = false
        for(j = 0; j < assigned_list.length; j++){
            //if queen (i) already in assigned_list skip thisi
            if(i == assigned_list[j]){
                already_assigned = true
                break
            }
        }
        if(already_assigned){
            continue
        }
        //here if i not assigned
        //find queen with fewest valid domain values
        //set best if not set yet
        if(best == null){
            best = i
            best_count = csp[0][i].length
            continue
        }
        //else
        var count = csp[0][i].length
        //compare best and i; set best if count < best_count
        if(count < best_count){
            best = i
            best_count = count
        }
    }
    return best
}
//===============================================
function checkSolution(queens, list){
    if(list.length == queens){
        return true
    }
    return false
}
//===============================================
function backtrack(csp, assigned_list){
    //call ac3 on the current csp and list of assigned queens
    //if ac3 is false(1 or more domains have no valid values)
    var results = ac3(csp)
    if(results == false){
        return false
    }
    csp = results[1]
    //check if the current csp is a solution
    if(checkSolution(csp[0].length,assigned_list)){
        return true
    }
    //get next queen to assign; put it in new list to pass on
    var var_to_assign = minimumRemainingValues(csp,assigned_list)
    var new_assigned_list = JSON.parse(JSON.stringify(assigned_list))//deep copy
    new_assigned_list.push(var_to_assign)
    /*
    set the var_to_assign
    loop through possible values of the queen
    set the new csp with domain updated with all -1 except
        the value we want
    set node to that new csp
    call backtrack on new csp
    if statements based on what backtrack return
    */
    var new_csp = null
    var root = null
    for(var i = 0; i < csp[0][var_to_assign].length; i++){//domain val i - chosen value
        new_csp = JSON.parse(JSON.stringify(csp))//deep copy
        for(var j = 0; j < csp[0][var_to_assign].length; j++){//loop through domain vals
            if(i != j){
                delete new_csp[0][var_to_assign][j]
            }
        }
        var row = []
        new_csp[0][i].forEach(function(element){
            if(element != undefined){
                row.push(element)
            }
        })
        new_csp[0][i] = row
        root = new Node(assigned_list, csp[0])
        var root_next = backtrack(new_csp, new_assigned_list)
        if(root_next == false){
            continue
        }
        if(root_next == true){
            root.next_node = new Node(new_assigned_list, new_csp[0])
            return root
        }
        else{
            root.next_node = root_next
            return root
        }
    }
    return false
}
//===============================================

/*
    WEB PAGE RELATED
*/
function setQueen(queen, domain, row){
    var result = []
    for(i = 0; i < domain; i++){
        if(i == (row-1)){
            result.push(i)
        }
    }
    return result
}
//===============================================
function getQueens(csp, assigned_list, data){
    if(data.size == 0){
        return [csp.assigned_list]
    }
    var l = csp[0][0].length
    for (var [key, value] of data.entries()) { 
        switch(key){
            case "q1":
                csp[0][0] = setQueen(0,l,value)
                assigned_list.push(0)
                break;
            case "q2":
                csp[0][1] = setQueen(1,l,value)
                assigned_list.push(1)
                break;
            case "q3":
                csp[0][2] = setQueen(2,l,value)
                assigned_list.push(2)
                break;
            case "q4":
                csp[0][3] = setQueen(3,l,value)
                assigned_list.push(3)
                break;
            case "q5":
                csp[0][4] = setQueen(4,l,value)
                assigned_list.push(4)
                break;
            case "q6":
                csp[0][5] = setQueen(5,l,value)
                assigned_list.push(5)
                break;
            case "q7":
                csp[0][6] = setQueen(6,l,value)
                assigned_list.push(6)
                break;
            case "q8":
                csp[0][7] = setQueen(7,l,value)
                assigned_list.push(7)
                break;
            case "q9":
                csp[0][8] = setQueen(8,l,value)
                assigned_list.push(8)
                break;
            case "q10":
                csp[0][9] = setQueen(9,l,value)
                assigned_list.push(9)
                break;
            case "q11":
                csp[0][10] = setQueen(10,l,value)
                assigned_list.push(10)
                break;
            case "q12":
                csp[0][11] = setQueen(11,l,value)
                assigned_list.push(11)
                break;
            case "q13":
                csp[0][12] = setQueen(12,l,value)
                assigned_list.push(12)
                break;
            case "q14":
                csp[0][13] = setQueen(13,l,value)
                assigned_list.push(13)
                break;
            case "q15":
                csp[0][14] = setQueen(14,l,value)
                assigned_list.push(14)
                break;
            case "q16":
                csp[0][15] = setQueen(15,l,value)
                assigned_list.push(15)
                break;
        }
      }
      return [csp, assigned_list]
    
}
//===============================================
function makeBoards(root,size){ //takes root node
    this_root = root
    this_root = this_root.next_node
    var l = size
    var board
    var a = 1
    while(this_root != null){
        board = "#board" + a
        var tabl = $(board)
        var str_to_add
        for(p = 0; p < l; p++){//row
            str_to_add = "<tr>"
            for(q = 0; q < l; q++){
                if(q%2 == 0){
                    str_to_add += "<td id='even'></td>"
                }
                else{
                    str_to_add += "<td id='odd'></td>"
                }
            }
            str_to_add += "</tr>"
            tabl.append(str_to_add)
        }
        this_root = this_root.next_node
        a++
    }
    //boards created
    //need to loop through reversed of normal
    //for each board
    this_root = root
    this_root = this_root.next_node
    var a = 0
    while(this_root != null){
        board = "board"+ (a+1)
        var tbl = document.getElementById(board)
        var rows = tbl.querySelectorAll('tr');
        for(i = 0; i < l; i++){//row
            var cells = rows[i].querySelectorAll('td');
            for(j = 0; j < l; j++){//col
                j_assigned = false
                for(p = 0; p < l; p++){
                    if(j == this_root.assigned_list[p]){
                        j_assigned = true
                        break
                    }
                }
                if(j_assigned){
                    //if assigned; its queen
                    if(this_root.vars_doms[j][0] == i){
                        cells[j].style.backgroundImage = "url('queen.png')"
                    } //else nothing
                    else {
                        cells[j].style.backgroundImage = ""
                    }
                    continue
                }
                is_valid = false
                for(r = 0; r < this_root.vars_doms[j].length; r++){
                    if(this_root.vars_doms[j][r] == i){
                        is_valid = true
                        break
                    }
                }
                if(!is_valid){
                    cells[j].style.backgroundImage = "url('redx.png')"
                }
            }
        }
        this_root = this_root.next_node
        a++
    }
}
//===============================================
function removeBoard(n){
    var l = n
    var board
    for(i = 0; i < l; i++){
        board = "#board" + (i+1) +" tr"
        $(board).each(function(){
            $(this).remove()
        })
    }
}
//===============================================
function printNode(root_node){
    while(root_node != null){
        console.log("\nassigned",root_node.assigned_list,"\nvars_doms\n",root_node.vars_doms)
        root_node = root_node.next_node
    }
}
//===============================================
/*
  TEST IN SHELL

  Output:
    assigned [ ]  -  This is a list of assigned queens in this step
    vars_doms - These are the domains of the queens in this step

  change the parameter in setup() to number of queens desired
*/

//UNCOMMENT BELOW THIS
//WARNING - keep below commented if runnig web page


var csp = setup(8)
var list = []
var root = backtrack(csp,list)
printNode(root)

