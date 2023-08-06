import numpy as np
from cryolo import utils
import tqdm
def convert_traces_to_bounding_boxes(traces):
    """
    Converts traces to a list of BoundingBox instances
    :param traces: Results of tracing
    :return: List of BoundingBox instances.
    """
    ccords = []
    for trace_id in np.unique(traces["particle"]):#range(num_particles):
        one_trace = traces[traces["particle"] == trace_id]

        xcoords = one_trace["x"].tolist()
        ycoords = one_trace["y"].tolist()
        zcoords = one_trace["frame"].tolist()
        widths = one_trace["widths"].tolist()
        heights = one_trace["heights"].tolist()
        confidence = one_trace["confidence"].tolist()
        est_box_widths = [meta["boxsize_estimated"][0] for meta in one_trace["meta"].tolist()]
        est_box_heights = [meta["boxsize_estimated"][1] for meta in one_trace["meta"].tolist()]

        x = np.mean(xcoords)
        y = np.mean(ycoords)
        z = np.mean(zcoords)
        w = np.mean(widths)
        h = np.mean(heights)
        c = np.mean(confidence)
        estimated_boxsize = (np.mean(est_box_widths),np.mean(est_box_heights))

        meta = {"boxsize_estimated": estimated_boxsize}
        meta["num_boxes"] = len(xcoords)
        bbox = utils.BoundBox(
            x=x,
            y=y,
            z=z,
            c=c,
            w=w,
            h=h,
            depth=w, # set it to same as the width. Should be a cube anyway.
            classes=[c]
        )
        bbox.meta = meta
        ccords.append(bbox)
    return ccords

def filaments_group_to_3D(filaments_df, window_size, box_distance):
    """
     For first filament: Subtract the first from
     last position and normalize the vector. This gives v0.
     v_avg = v0
     For each other filament
         Subtract(Last,First) and normalize -> v_k
         if v_k dot v_avg > 0:
           v_avg += v_k
           v_avg = norm(v_avg)
     Sort all filament positions along v_avg
     Running moving average along v_avg
     Resample


    :param filaments_df:
    :return:
    """

    def normalize_vec(vec):
        norm = np.linalg.norm(vec)
        if norm == 0:
            return vec
        return vec / norm

    def filament_direction_np(A):
        Acentered = A - A.mean(axis=0)
        Acov = np.zeros(shape=(2,2))
        #np.matmul(Acentered.T, Acentered, out=Acov)
        Acov = np.dot(Acentered.T, Acentered)
        evals, evecs = np.linalg.eigh(Acov)
        result = evecs[:, np.argmax(evals)]

        return result

    def filament_direction(fil):
        A = fil[["x","y"]]
        return filament_direction_np(A)

    nphelp = filaments_df["width"].to_numpy()
    same_box_size = (np.abs(nphelp-nphelp[0])<10**-6).all()

    assert same_box_size, print("The filaments have to have the same box size. Exit.")
    boxsize = nphelp[0]

    '''
    Calculate average direction v_avg in 2D of all filaments 
    '''
    fids = np.unique(filaments_df["fid"].tolist())
    pos = []
    for fid in fids:
        filament_trace = filaments_df[filaments_df["fid"] == fid]
        pos.append(filament_trace[["x","y"]])
    pos_help = np.concatenate(pos)
    v_avg = filament_direction_np( pos_help)

    '''
     Sort them according their x,y coordinates.
    '''
    xs = []
    ys = []
    zs = []
    conf=[]
    for fid in fids:
        filament_trace = filaments_df[filaments_df["fid"] == fid]
        xs.extend(filament_trace["x"].tolist())
        ys.extend(filament_trace["y"].tolist())
        zs.extend(filament_trace["frame"].tolist())
        conf.extend(filament_trace["confidence"].tolist())


    xs = np.array(xs)
    ys = np.array(ys)
    zs = np.array(zs)
    conf = np.array(conf)

    dotproducts = []
    for i in range(len(xs)):
        dp = np.dot(
            v_avg,
            np.array([xs[i], ys[i]])
        )
        dotproducts.append(
            dp
        )
    dotproducts = np.array(dotproducts)
    sorted_coords_indicis = np.argsort(dotproducts)
    xs = xs[sorted_coords_indicis]
    ys = ys[sorted_coords_indicis]
    zs = zs[sorted_coords_indicis]
    conf = conf[sorted_coords_indicis]
    dotproducts = dotproducts[sorted_coords_indicis]


    '''
    Moving average
    '''
    w = window_size
    boxes_3d = []

    for i in range(int(min(dotproducts)),int(max(dotproducts))+1):
        window_elements = np.logical_and(dotproducts > (i-w/2), dotproducts<i+w/2)

        if np.sum(window_elements) > 0:
            x3d = np.mean(xs[window_elements])
            y3d = np.mean(ys[window_elements])
            z3d = np.mean(zs[window_elements])
            conf3d = np.mean(conf[window_elements])

            box3d = utils.BoundBox(x=x3d,y=y3d,z=z3d, w=boxsize,h=boxsize,depth=boxsize,c=conf3d)
            box3d.meta["num_boxes"] = len(np.unique(zs[window_elements]))
            if len(boxes_3d)==0:
                boxes_3d.append(box3d)
            elif not np.allclose(
                    [boxes_3d[-1].x, boxes_3d[-1].y, boxes_3d[-1].z],
                    [x3d,y3d,z3d]
            ):
                boxes_3d.append(box3d)
            else:
                pass


    '''
    resample
    '''
    new_fil = utils.Filament(boxes=boxes_3d)
    resampled_filament = utils.resample_filaments([new_fil], box_distance)

    if len(resampled_filament) > 0:
        return resampled_filament[0]

    return None

def get_local_filament_direction(position, boxes, radius=2):

    from_i = max(0, position-radius)
    to_i = min(position+radius,len(boxes)-1)
    if from_i == to_i:
        return np.array([0,0])
    dx = boxes[from_i].x - boxes[to_i].x
    dy = boxes[from_i].y - boxes[to_i].y

    dvec = np.array([dx,dy])
    dvec = dvec / np.linalg.norm(dvec)
    return dvec
from typing import List, Tuple

def get_edge_histogram( edges: List[Tuple]) -> Tuple[np.array, List[Tuple]]:
    edgeset = set()
    edgeset.update(edges)
    bin_edges = list(edgeset)
    hist = np.zeros(len(bin_edges))
    for e in tqdm.tqdm(edges,desc="Calculate edge histogram"):
        i = bin_edges.index(e)
        hist[i] = hist[i] + 1

    return hist, bin_edges

def do_tracing_filaments(filaments_dict,
               search_range=5,
               memory=3,
               confidence_threshold=0,
               min_edge_weight=0,
               window_size=2,
               box_distance=1,
               resample_dist=-1,
               min_length_filament=0,
               iou_threshold=0.3,
               merge_threshold=0.8):
    '''

    :param filaments_dict: Filament dictionary. keys are the frame numbers
    :param search_range: Search range for tracing along z
    :param memory: Memory (allowed gap size during training)
    :param confidence_threshold: Confidence threshold
    :param min_edge_weight: Minimum edge weight. Edges shorts than this got removed
    :param window_size:
    :param box_distance:
    :param resample_dist:
    :param min_length_filament:
    :param iou_threshold:
    :param merge_threshold:
    :return:
    '''
    import pandas as pd
    import trackpy as tp
    import sys
    coords_and_frame = {
        "x": [],
        "y": [],
        "frame": [],
        "fid": [],
        "confidence":[],
        "width":[],
        "height":[],
        "meta":[],
        "fdirection":[]
    }
    fid = 0
    num_box = 0
    print("..Convert and resample")
    def printfilament(f):
        print("X", [b.x for b in f.boxes])
        print("Y", [b.y for b in f.boxes])
        print("Z", [b.y for b in f.boxes])

    for frame_number in filaments_dict:

        if resample_dist == -1:
            resampled_filaments = utils.resample_filaments(filaments_dict[frame_number],2*search_range+1)


        elif resample_dist > 0:

            resampled_filaments = utils.resample_filaments(filaments_dict[frame_number],
                                                           resample_dist)

        for filament_index, filament in enumerate(resampled_filaments):
            for box_i, box in enumerate(filament.boxes):
                if box.c > confidence_threshold:
                    coords_and_frame["x"].append(box.x)
                    coords_and_frame["y"].append(box.y)
                    coords_and_frame["frame"].append(frame_number)
                    coords_and_frame["fid"].append(fid)
                    coords_and_frame["confidence"].append(box.c)
                    coords_and_frame["meta"].append(box.meta)
                    coords_and_frame["width"].append(box.w)
                    coords_and_frame["height"].append(box.h)
                    coords_and_frame["fdirection"].append(get_local_filament_direction(position=box_i, boxes=filament.boxes, radius=2))
                    num_box = num_box + 1
            filaments_dict[frame_number][filament_index].meta["group3d_fid"] = fid
            fid = fid + 1
    if len(coords_and_frame["x"])==0:
        return []
    coords_frame_df = pd.DataFrame(coords_and_frame)


    tp.quiet(True)
    #import trackpy.linking as lnkng
    #lnkng.linking.Linker.MAX_SUB_NET_SIZE=50
    '''
    print("memory", memory)
    print("searchrange", search_range)
    print("windowsize", window_size)
    print("min_edge", min_edge_weight)
    print("conf", confidence_threshold)
    print("widht", coords_frame_df["width"][0])
    print("maxmin", np.max(coords_frame_df["x"]),np.min(coords_frame_df["x"]))
    '''
    #print("SUBETCONF:", lnkng.linking.Linker.MAX_SUB_NET_SIZE,lnkng.linking.Linker.MAX_SUB_NET_SIZE_ADAPTIVE, memory*search_range+1)
    print("..Trace", "SR", search_range, "MEM", memory)
    coords_frame_traced_df = tp.link_df(coords_frame_df,
                                        search_range=search_range,
                                        adaptive_stop = 2,
                                        adaptive_step = 0.8,
                                        memory=memory)

    #print("Linking done")
    print("..Build graph")
    # Next steps:
    # Build graph
    #np.unique(coords_frame_traced_df["particle"])
    import networkx as nx

    edges = []
    nodes = []
    all_r_values = []
    import tqdm

    for trace_id in tqdm.tqdm(np.unique(coords_frame_traced_df["particle"]), desc="Find nodes"):
        one_trace = coords_frame_traced_df[coords_frame_traced_df["particle"] == trace_id]

        '''
        filament_directions = one_trace["fdirection"].tolist()
        exceeded = False

        for i in range(len(filament_directions)-1):
            r = np.linalg.norm(np.cross(filament_directions[i], filament_directions[i+1]))
            all_r_values.append(r)
            if r > 0.15:
                exceeded = True
        if exceeded:
            pass
            #print("Exceeded!", r)
            #continue
        '''

        trace_fid_list = one_trace["fid"].tolist()
        for i in range(len(trace_fid_list)-1):
            edge = tuple(sorted((trace_fid_list[i],trace_fid_list[i+1])))
            edges.append(edge)
        nodes.extend(trace_fid_list)

    # Add nodes + Calculate edge weight + add weights
    nodes = set(nodes)

    G = nx.Graph()
    for node in nodes:
        G.add_node(node)

    thefids = coords_frame_traced_df["fid"]
    histfids, histfids_bins = np.histogram(thefids.values,bins=range(max(thefids)-min(thefids)+2))
    assert histfids_bins[0]==0
    hist_edges, hist_edges_bin = get_edge_histogram(edges)

    for edge in tqdm.tqdm(edges, desc="Build edges"):
        edge_weight = hist_edges[hist_edges_bin.index(edge)]#len([i for i,an_edge in enumerate(edges) if an_edge == edge])
        #print(edge_weight, hist_edges[hist_edges_bin.index(edge)])
        fil_length_a = histfids[edge[0]]#np.count_nonzero(thefids == edge[0])

        fil_length_b = histfids[edge[1]]#np.count_nonzero(thefids == edge[1])

        min_length = min(fil_length_a,fil_length_b)
        max_length = max(fil_length_a,fil_length_b)
        edge_weight = edge_weight/min_length * np.sqrt(min_length/max_length)
        has_minimum_weight = edge_weight >= min_edge_weight
        if has_minimum_weight:
            G.add_edge(edge[0],edge[1],weight=edge_weight)

    print("..Find connected components")
    # Find connected components
    connected_components = nx.connected_components(G)

    # Generate one 3D trace per connected component
    filaments_3d = []
    print("..Convert CCs to 3D Filaments")



    for sub in tqdm.tqdm(connected_components, desc="Convert to 3D"):
        filaments_of_cc = coords_frame_traced_df[ coords_frame_traced_df["fid"].isin(sub)]
        if len(filaments_of_cc.index) > 1:
            f3d = filaments_group_to_3D(filaments_of_cc, window_size=window_size, box_distance=box_distance)

            if f3d is not None:
                    filaments_3d.append(f3d)
                    f3d.meta["group3d_fids"] = sub

    '''
    Merge overlaping 3d filaments based on IOU
    '''
    print("..Merge strongly overlapping 3D Filaments", len(filaments_3d))
    filaments_3d = utils.merge_filaments_3d(filaments_3d,
                                            iou_threshold=iou_threshold,
                                            merge_threshold=merge_threshold,
                                            window_radius=window_size,
                                            box_distance=box_distance)
    print("..Merge partially ", len(filaments_3d))

    filaments_3d = utils.merge_filaments_3d(filaments_3d,
                                            iou_threshold=iou_threshold,
                                            merge_threshold=0,
                                            window_radius=window_size,
                                            box_distance=box_distance,
                                            partial=True)
    print("..Done", len(filaments_3d))
    print("Remove filaments shorter then:", min_length_filament)
    filaments_3d = [fil for fil in filaments_3d if len(fil.boxes)>=min_length_filament]

    print("..Done", len(filaments_3d))
    return filaments_3d


def do_tracing(boxes_dict,
               search_range=5,
               memory=3,
               confidence_threshold=0,
               min_length=5):
    """
    Will trace the boxes

    :param boxes_dict: Dictonary of lists of BoundingBox instances. Key the is the frame number.
    :param search_range: Maximum distance between position to get linked
    :param memory: Maximum gap in z direction.
    :param min_length: Minimum number of points (boxes in one  trace (default 5)
    :param confidence_threshold: Ignores boxes in boxes_list which have a confidence lower than this threshold
    :return: List of 3D bounding boxes
    """
    import pandas as pd
    import trackpy as tp
    coords_and_frame = {"x": [], "y": [], "frame": []}
    confidences = []
    meta = []
    widths = []
    heights = []
    for frame_number  in boxes_dict:
        for box in boxes_dict[frame_number]:
            if box.c > confidence_threshold:
                coords_and_frame["x"].append(box.x)
                coords_and_frame["y"].append(box.y)
                coords_and_frame["frame"].append(frame_number)
                confidences.append(box.c)
                meta.append(box.meta)
                widths.append(box.w)
                heights.append(box.h)
                assert len(box.classes) == 1, "for classes > 1 we need to complete the implementation"
    if len(coords_and_frame["x"])==0:
        return []
    coords_frame_df = pd.DataFrame(coords_and_frame)

    tp.quiet(True)
    coords_frame_traced_df = tp.link_df(coords_frame_df,
                                       search_range=search_range,
                                       memory=memory)
    coords_frame_traced_df["confidence"] = confidences
    coords_frame_traced_df["meta"] = meta
    coords_frame_traced_df["widths"] = widths
    coords_frame_traced_df["heights"] = heights
    coords_frame_traced_df= tp.filter_stubs(coords_frame_traced_df, min_length)
    boxes = convert_traces_to_bounding_boxes(coords_frame_traced_df)
    return boxes

def do_cluster(boxes_list,max_dist=2,max_z=3, confidence_threshold=0.3):

    num_boxes = np.sum([len([box for box in boxes if box.c>confidence_threshold]) for boxes in boxes_list])

    data = np.zeros(shape=(num_boxes,3))
    k = 0
    for boxes_index, boxes in enumerate(boxes_list):
        for box in boxes:
            if box.c > confidence_threshold:
                data[k,0]=box.x
                data[k,1]=box.y
                data[k,2]=boxes_index
                k = k + 1
    from sklearn import cluster
    epsilon = np.sqrt(max_dist * max_dist + max_z * max_z)

    clustering = cluster.AgglomerativeClustering(n_clusters=None, distance_threshold=80).fit(data) #cluster.DBSCAN(eps=epsilon, min_samples=3).fit(data)

    print("Num clusters found:", len(set(clustering.labels_)))

    return None#NotImplementedError("This method is not implemented yet")
